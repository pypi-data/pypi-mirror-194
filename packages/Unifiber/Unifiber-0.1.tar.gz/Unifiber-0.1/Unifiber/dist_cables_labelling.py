from qgis.core import *
from PyQt5.QtCore import QVariant
import os,sys
import shutil
import fileinput
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import pandas as pd
import time
from tools import tools
#create instance
copyFeatures = tools.CopyFeatures(iface)


""" log
v2.1=bug fixes
v2.0=tools sync, QA, bug fixes
v1.4="A/F/K" in labels | output.txt file | fixed copies bugs
v1.3=redefined "K" count for cable type changes | minor modifications
v1.2=modified count structure
v1.1=adapted for add the cables to specified labels
v1.0=first dev version
"""

def distCables():

    #DEF
    prj = QgsProject.instance()
    prjTitle = prj.title()
    start_time = time.time()    #Timer

    #SHAPES DE ENTRADA
    print('>Layers')
    CABLE = prj.mapLayersByName('Distribution Cables')[0]
    DP = prj.mapLayersByName('DP')[0]
    RISER = prj.mapLayersByName('Riser')[0]
    POLE = prj.mapLayersByName('Pole Closure')[0]
    FACADE = prj.mapLayersByName('FacadeClosure')[0]
    BOX = prj.mapLayersByName('TerminationBox')[0]
    CO = prj.mapLayersByName('CO')[0]
    DHH = prj.mapLayersByName('DHH')[0]
    BK = prj.mapLayersByName('BK')[0]

    root = prj.layerTreeRoot()

    #GEOMETRIES
    ##JUNTA TODOS OS PONTOS
    print('>Geometries')
    PONTOS = processing.run("native:mergevectorlayers", 
    {'LAYERS':[DP,RISER,POLE,FACADE,BOX,CO,DHH,BK],
    'CRS':QgsCoordinateReferenceSystem('EPSG:31370'),
    'OUTPUT':'TEMPORARY_OUTPUT'})

    ##ATUALIZA O CAMPO ID
    PONTOS = processing.run("native:fieldcalculator", 
    {'INPUT':PONTOS['OUTPUT'],
    'FIELD_NAME':'ID',
    'FIELD_TYPE':2,
    'FIELD_LENGTH':250,
    'FIELD_PRECISION':0,
    'FORMULA':"$ID",
    'OUTPUT':'TEMPORARY_OUTPUT'})

    ##ATRAI AS LINHAS AOS PONTOS
    LINHAS = processing.run("native:snapgeometries", 
    {'INPUT':CABLE,
    'REFERENCE_LAYER':PONTOS['OUTPUT'],
    'TOLERANCE':0.1,
    'BEHAVIOR':0,
    'OUTPUT':'TEMPORARY_OUTPUT'})

    ##ADICIONA A CAMADA TEMPORÁRIA AO MAPA
    prj.addMapLayer(PONTOS['OUTPUT'])

    ##CAMPOS DE ORIGEM E DESTINO
    LINHAS = processing.run("native:fieldcalculator", 
    {'INPUT':LINHAS['OUTPUT'],
    'FIELD_NAME':'ORIGEM',
    'FIELD_TYPE':2,
    'FIELD_LENGTH':250,
    'FIELD_PRECISION':0,
    'FORMULA':"aggregate(\r\nlayer:= 'Calculated',\r\naggregate:='concatenate',\r\nexpression:= to_string(ID),\r\nconcatenator:=',',\r\nfilter:=intersects($geometry, start_point(geometry(@parent))))\r\n",'OUTPUT':'TEMPORARY_OUTPUT'})

    LINHAS = processing.run("native:fieldcalculator", 
    {'INPUT':LINHAS['OUTPUT'],
    'FIELD_NAME':'DESTINO',
    'FIELD_TYPE':2,
    'FIELD_LENGTH':250,
    'FIELD_PRECISION':0,
    'FORMULA':"aggregate(\r\nlayer:= 'Calculated',\r\naggregate:='concatenate',\r\nexpression:= to_string(ID),\r\nconcatenator:=',',\r\nfilter:=intersects($geometry, end_point(geometry(@parent))))\r\n",'OUTPUT':'TEMPORARY_OUTPUT'})

    CABLE_FINAL = processing.run("native:addfieldtoattributestable", 
    {'INPUT':LINHAS['OUTPUT'],
    'FIELD_NAME':'Label',
    'FIELD_TYPE':2,
    'FIELD_LENGTH':150,
    'FIELD_PRECISION':0,
    'OUTPUT':'TEMPORARY_OUTPUT'})

    ##ADICIONA A CAMADA TEMPORÁRIA AO MAPA
    #prj.addMapLayer(LINHAS['OUTPUT'])
    prj.addMapLayer(CABLE_FINAL['OUTPUT'])

    #CABLE = CABLE_FINAL['OUTPUT']
    #PONTOS = PONTOS['OUTPUT']
    CABLE = prj.mapLayersByName('Added')[0]
    PONTOS = prj.mapLayersByName('Calculated')[0]

    ##CRIANDO DF COM TABELA DE PONTOS
    print('>DF')
    cols = [f.name() for f in PONTOS.fields()] 
    dados = ([f[col] for col in cols] for f in PONTOS.getFeatures())
    df_PONTOS = pd.DataFrame.from_records(data=dados, columns=cols)

    ##CRIANDO DF COM TABELA DE PONTOS
    cols = [f.name() for f in CABLE.fields()] #Or list them manually: ['kommunnamn', 'kkod', ... ]
    dados = ([f[col] for col in cols] for f in CABLE.getFeatures())
    df_CABLE = pd.DataFrame.from_records(data=dados, columns=cols)

    ##CRIANDO DATAFRAME VAZIO
    colunas = ['ID','DP','EXTREMIDADE','TAMANHO','K','R','Q']
    df = pd.DataFrame(columns=colunas)

    ##CRIA LISTAS DE ORIGEM E DESTINO
    origem = []
    extremidade = []
    for feature in CABLE.getFeatures():
        origem.append(feature["ORIGEM"]) 
        extremidade.append(feature["DESTINO"]) 

    ##ENCONTRA AS EXTREMIDADES DO PROJETO 
    pontos_finais = [i for i in extremidade if i not in origem]

    """MAIN LOOPS"""
    ## LOOP PARA COLETAR A QUANTIDADE DE CABOS ATÉ CHEGAR NO DP
    print('>Loop #1')
    for ponto_final in pontos_finais:
        x=0
        #print(ponto_final,x)
        destino = ponto_final
        while True:
            extremidade = ponto_final        
            cable_filter = df_CABLE.loc[df_CABLE['DESTINO'] == extremidade]
            try:
                ponto_final = cable_filter.iloc[0]['ORIGEM']
            except:
                print('     [ERROR] - loop #1, item {}'.format(ponto_final))
                break
            x+=1
            #print(ponto_final,x)
            
            ORIGEM = df_PONTOS.loc[df_PONTOS['ID'] == int(ponto_final)]
            layer = ORIGEM.iloc[0]['layer']
            name_dp = ORIGEM.iloc[0]['Label']
            id_dp = ORIGEM.iloc[0]['ID']

            if layer == 'DP':
                break
        
        new_row = {'ID': id_dp,'DP': name_dp,'EXTREMIDADE':destino,'TAMANHO':x,'K':0,'R':0,'Q':0}
        df = df.append(new_row, ignore_index=True)
    df = df.sort_values(['ID', 'TAMANHO'],ascending=False)


    ## LOOP PARA CORRIGIR A QUANTIDADE DE CABOS ATÉ A DERIVAÇÃO
    print('>Loop #2')
    K_deriv = 1 #0
    ID_ANTIGO = 0
    lista = []
    for i in range(len(df)):
        type_anterior = ''
        x=0
        TAMANHO = df.iloc[i]['TAMANHO']
        ID = df.iloc[i]['ID']
        DP = df.iloc[i]['DP']
        EXTREMIDADE = df.iloc[i]['EXTREMIDADE']
        ponto_final = EXTREMIDADE

        K_deriv += 1
        if ID_ANTIGO != ID:
            K_deriv = 1
        ID_ANTIGO = ID
            
        R = 0
        Q = 0   #1
        #inner loop
        while True:
            lista.append(ponto_final)
            #print(lista)
            extremidade = ponto_final

            #LINE FILTER
            cable_filter = df_CABLE.loc[df_CABLE['DESTINO'] == extremidade]
            try:
                ponto_final = cable_filter.iloc[0]['ORIGEM']
                type_atual = cable_filter.iloc[0]['Type']
            except:
                print('     [ERROR] - loop #2, item {}'.format(ponto_final))
                break
            x+=1
            
            #INFO
            ORIGEM = df_PONTOS.loc[df_PONTOS['ID'] == int(ponto_final)]
            layer = ORIGEM.iloc[0]['layer']
            id_dp = ORIGEM.iloc[0]['ID']
                
            if layer == 'Riser':
                R += 1
            #print('[{}]'.format(name_dp),ponto_final,'-',type_atual,K_deriv,Q)

            if type_atual != type_anterior and type_anterior!='':
                Q+=1
            type_anterior = type_atual

            #BREAKS
            if layer == 'DP':
                #K_deriv+=1
                #name_dp = ORIGEM.iloc[0]['Label']
                break

            if ponto_final in lista:
                break

        df.iloc[i]['TAMANHO'] = x
        df.iloc[i]['K'] = K_deriv
        df.iloc[i]['R'] = R
        df.iloc[i]['Q'] = Q

        K_deriv = K_deriv + Q
    df = df.sort_values(['ID','K', 'TAMANHO'],ascending=False)
    #print(df.to_string())


    #ADICIONANDO AO MAPA E ATIVANDO EDIÇÃO
    CABLE_FINAL = prj.mapLayersByName('Added')[0]
    CABLE_FINAL.startEditing()

    #ENCONTRANDO O ID DO CAMPO LABEL
    fields = CABLE_FINAL.fields()
    idxEdgeId = fields.indexFromName('Label')

    ## LOOP PARA PREENCHER A LABEL
    print('>Loop #3')
    ID_ANTIGO = 0
    K_ANTIGO = 0
    #determina o primeiro ciclo

    for i in range(len(df)):
        type_anterior = ''
        #busca info de cada ramo em df
        ID = df.iloc[i]['ID']
        DP = df.iloc[i]['DP']
        EXTREMIDADE = df.iloc[i]['EXTREMIDADE']
        TAMANHO = df.iloc[i]['TAMANHO']
        K = df.iloc[i]['K']
        R = df.iloc[i]['R']
        Q = df.iloc[i]['Q']

        kq = Q+K
        ponto_final = EXTREMIDADE
        
        #print(ID_ANTIGO,ID)
        if ID_ANTIGO != ID: #se mudar de DP
            TAMANHO_S = 0
        
        #INNER
        while True:
            TAMANHO_S = TAMANHO
            extremidade = ponto_final
            ponto_final_2 = ponto_final

            #LINE FILTER
            cable_filter = df_CABLE.loc[df_CABLE['DESTINO'] == extremidade] #retorna a lista das extremidades
            try:
                type_atual = cable_filter.iloc[0]['Type']
            except:
                print('     [ERROR] - loop #3.1, item {}'.format(ponto_final))
                break

            S=0
            #INNER INNER
            while True:
                extremidade_2 = ponto_final_2
                #print(ponto_final,' - ',ponto_final_2)
                #LINE FILTER
                cable_filter_2 = df_CABLE.loc[df_CABLE['DESTINO'] == extremidade_2]
                try:
                    ponto_final_2 = cable_filter_2.iloc[0]['ORIGEM']
                    type_atual_2 = cable_filter_2.iloc[0]['Type']
                except:
                    print('     [ERROR] - loop #3.2, item {}'.format(extremidade_2))
                    break

                ORIGEM_2 = df_PONTOS.loc[df_PONTOS['ID'] == int(extremidade_2)]
                D_layer_2 = ORIGEM_2.iloc[0]['layer']

                if type_atual == '24v STC' or type_atual == '96v U-STC' or type_atual == '192 U-STC':
                    t = 'A-' #Aerial
                elif type_atual == 'Rectractanet 96FO':
                    t = 'F-' #Façade
                elif type_atual == '24v LTMC' or type_atual == '48v LTMC' or type_atual == '96v LTMC':
                    t = 'K-' #underground
                else:
                    t = ''

                # BREAKS
                if type_atual != type_atual_2:
                    break

                if D_layer_2 != 'Riser':
                    S += 1

                TAMANHO_S -= 1
                if TAMANHO_S <= 0:
                    break
            if S == 0:
                S = 1

            #TYPE
            if type_atual != type_anterior and type_anterior != '':
                kq -= 1

            ## ATUALIZAR O S QUANDO MUDAR O TYPE
            type_anterior = type_atual

            #LABEL POSITIONING
            origem = CABLE_FINAL.getFeatures("DESTINO LIKE '"+extremidade+"'")  #return 1 line/loop
            for feature in origem:
                ponto_final = feature["ORIGEM"]
                CABLE_FINAL.changeAttributeValue(feature.id(), idxEdgeId, t + str(DP) + '-K' + str(kq).zfill(2) + '-S' +  str(S).zfill(2))

            DESTINO = df_PONTOS.loc[df_PONTOS['ID'] == int(ponto_final)]
            D_layer = DESTINO.iloc[0]['layer']

            TAMANHO -= 1
            #BREAK
            if TAMANHO == 0:
                break
        x+=1
        ID_ANTIGO = ID

    CABLE_FINAL.setSubsetString("")
    CABLE_FINAL.commitChanges()

    #CLEAR INFO
    CABLE = prj.mapLayersByName('Distribution Cables')[0]
    #remove info in origin lyrs
    for f in CABLE.getFeatures():
        CABLE.startEditing()
        CABLE.deleteFeature(f.id())

    #COPIES
    print('>Copies')
    _temp_lines = prj.mapLayersByName('Added')[0]
    copyFeatures.copyAll(_temp_lines,CABLE)

    ohDist_lyr = prj.mapLayersByName("Dist Cables - OH")[0]
    #copyFeatures.copyByExp(CABLE,ohDist_lyr,'\"Type\"= \'24v STC\'')
    #copyFeatures.copyByExp(CABLE,ohDist_lyr,'\"Type\"= \'96v U-STC\'')
    #copyFeatures.copyByExp(CABLE,ohDist_lyr,'\"Type\"= \'192 U-STC\'')
    copyFeatures.copyByExp(CABLE,ohDist_lyr,'\"Spec\"= \'7\'')

    ugDist_lyr = prj.mapLayersByName("Dist Cables - UG")[0]
    #copyFeatures.copyByExp(CABLE,ugDist_lyr,'\"Type\"= \'24v LTMC\'')
    #copyFeatures.copyByExp(CABLE,ugDist_lyr,'\"Type\"= \'48v LTMC\'')
    #copyFeatures.copyByExp(CABLE,ugDist_lyr,'\"Type\"= \'96v LTMC\'')
    copyFeatures.copyByExp(CABLE,ugDist_lyr,'\"Spec\"= \'3\'')

    fcDist_lyr = prj.mapLayersByName("Dist Cables - FC")[0]
    #copyFeatures.copyByExp(CABLE,fcDist_lyr,'\"Type\"= \'Rectractanet 96FO\'')
    copyFeatures.copyByExp(CABLE,fcDist_lyr,'\"Spec\"= \'10\'')
    tools.ClearSelection()

    prj.removeMapLayer(prj.mapLayersByName('Added')[0].id())
    prj.removeMapLayer(prj.mapLayersByName('Calculated')[0].id())


    #EXPORT .TXT INFO
    #CABLES
    print('> Distribution_Cables.txt File')
    # specify the path to the layer
    layer = prj.mapLayersByName('Distribution Cables')[0]

    # specify the path to the output text file
    project_path = prj.readPath("./")
    output_path = project_path + "/Distribution_Cables_output.txt"

    # the index name to filter by
    handle_idx = "Handle"
    label_idx = "Label"

    # open the output file
    with open(output_path, 'w') as f:
        # get the fields in the layer
        fields = layer.fields()

        # write the field names as the header of the text file
        handle_head = [field.name() for field in fields if field.name() == handle_idx]
        label_head = [field.name() for field in fields if field.name() == label_idx]
        f.write("\t".join(handle_head) +','+ "\t".join(label_head) + "\n")

        # get the features in the layer
        features = layer.getFeatures()

        # write the attribute values for each feature
        for feature in features:
            h_values = [str(feature[field.name()]) for field in fields if field.name() == handle_idx]
            l_values = [str(feature[field.name()]) for field in fields if field.name() == label_idx]
            f.write("\t".join(h_values) +','+ "\t".join(l_values) + "\n")
    #DP
    print('> DP.txt File')
    # specify the path to the layer
    layer = prj.mapLayersByName('DP')[0]
    output_path = project_path + "/DP_output.txt"
    # open the output file
    with open(output_path, 'w') as f:
        # get the fields in the layer
        fields = layer.fields()

        # write the field names as the header of the text file
        handle_head = [field.name() for field in fields if field.name() == handle_idx]
        label_head = [field.name() for field in fields if field.name() == label_idx]
        f.write("\t".join(handle_head) +','+ "\t".join(label_head) + "\n")

        # get the features in the layer
        features = layer.getFeatures()

        # write the attribute values for each feature
        for feature in features:
            h_values = [str(feature[field.name()]) for field in fields if field.name() == handle_idx]
            l_values = [str(feature[field.name()]) for field in fields if field.name() == label_idx]
            f.write("\t".join(h_values) +','+ "\t".join(l_values) + "\n")


    print('========================================')
    print("--- END in %s seconds ---" % (time.time() - start_time))
    print('========================================')