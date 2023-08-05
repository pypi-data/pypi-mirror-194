from qgis.core import *
from PyQt5.QtCore import QVariant
import os
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
v2.0=tools sync, QA, bug fixes
v1.0=first dev version
"""
def feederCables():
    #DEF
    prj = QgsProject.instance()
    prjTitle = prj.title()
    start_time = time.time()    #Timer

    #SHAPES DE ENTRADA
    print('>Layers')
    CABLE = prj.mapLayersByName('Feeder Cable')[0]
    DP = prj.mapLayersByName('DP')[0]
    BK = prj.mapLayersByName('BK')[0]
    RISER = prj.mapLayersByName('Riser')[0]
    CO = prj.mapLayersByName('CO')[0]

    #SET LABELS NULL
    CABLE.startEditing()
    e = QgsExpression('NULL')
    c = QgsExpressionContext()
    s = QgsExpressionContextScope()
    s.setFields(CABLE.fields())
    c.appendScope(s)
    e.prepare(c)

    lb_idx = CABLE.fields().lookupField('Label')

    for f in CABLE.getFeatures():
        c.setFeature(f)
        value = e.evaluate(c)
        atts = {lb_idx: value}
        CABLE.changeAttributeValues(f.id(), atts)
    CABLE.commitChanges()
    CABLE = prj.mapLayersByName('Feeder Cable')[0]     #update value

    #GEOMETRIES
    ##JUNTA TODOS OS PONTOS
    print('>Geometries')
    PONTOS = processing.run("native:mergevectorlayers", 
    {'LAYERS':[DP,RISER,CO,BK],
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


    ##ADICIONA A CAMADA TEMPORÁRIA AO MAPA
    QgsProject.instance().addMapLayer(PONTOS['OUTPUT'])

    ##CAMPOS DE ORIGEM E DESTINO
    LINHAS = processing.run("native:fieldcalculator", 
    {'INPUT':CABLE,
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
    #QgsProject.instance().addMapLayer(LINHAS['OUTPUT'])
    QgsProject.instance().addMapLayer(CABLE_FINAL['OUTPUT'])


    CABLE = CABLE_FINAL['OUTPUT']
    PONTOS = PONTOS['OUTPUT']

    ##CRIANDO DF COM TABELA DE PONTOS
    print('>DF')
    cols = [f.name() for f in PONTOS.fields()] 
    dados = ([f[col] for col in cols] for f in PONTOS.getFeatures())
    df_PONTOS = pd.DataFrame.from_records(data=dados, columns=cols)

    ##CRIANDO DF COM TABELA DE CABOS
    cols = [f.name() for f in CABLE.fields()] #Or list them manually: ['kommunnamn', 'kkod', ... ]
    dados = ([f[col] for col in cols] for f in CABLE.getFeatures())
    df_CABLE = pd.DataFrame.from_records(data=dados, columns=cols)

    ##CRIANDO DATAFRAME VAZIO
    colunas = ['ID','DP','EXTREMIDADE','TAMANHO']
    df = pd.DataFrame(columns=colunas)



    ##CRIA LISTAS DE  DESTINO
    extremidade = []
    todos_destinos = df_CABLE.DESTINO.unique()

    for destino in todos_destinos:
        df_cable_origem = df_CABLE.loc[df_CABLE['ORIGEM'] == destino]
        df_cable_destino = df_CABLE.loc[df_CABLE['DESTINO'] == destino]
        if len(df_cable_origem)!=len(df_cable_destino):
            extremidade.append(destino)
        
    print(todos_destinos,extremidade)
    #df_dp = df_PONTOS.loc[df_PONTOS['layer'] == 'DP']

    """MAIN LOOPS"""
    #LOOP PARA COLETAR A QUANTIDADE DE CABOS ATÉ CHEGAR NO CO
    print('>Loop #1')
    for ponto_final in extremidade:
        x=0
        print(ponto_final,x)
        destino = ponto_final
        
        
        df_dp = df_PONTOS.loc[df_PONTOS['ID'] == int(ponto_final)]
        name_dp = df_dp.iloc[0]['Label']
        id_dp = df_dp.iloc[0]['ID']

        while True:
            extremidade = ponto_final        
            
            cable_filter = df_CABLE.loc[df_CABLE['DESTINO'] ==  str(extremidade)]
        
            try:
                ponto_final = cable_filter.iloc[0]['ORIGEM']
            except:
                break
                
            x+=1
            print(ponto_final,x)
            
            ORIGEM = df_PONTOS.loc[df_PONTOS['ID'] == int(ponto_final)]
            layer = ORIGEM.iloc[0]['layer']


            if layer == 'CO':
                break
        
        new_row = {'ID': id_dp,'DP': name_dp,'EXTREMIDADE':str(destino),'TAMANHO':x}
        df = df.append(new_row, ignore_index=True)

    df = df.sort_values(['TAMANHO'],ascending=True)
    print(df)


    #ADICIONANDO AO MAPA E ATIVANDO EDIÇÃO
    CABLE_FINAL = prj.mapLayersByName('Added')[0]
    CABLE_FINAL.startEditing()

    #ENCONTRANDO O ID DO CAMPO LABEL
    fields = CABLE_FINAL.fields()
    idxEdgeId = fields.indexFromName('Label')

    #LOOP PARA PREENCHER A LABEL
    print('>Loop #2')
    k = 0
    for i in range(len(df)):
        TAMANHO = df.iloc[i]['TAMANHO']
        NAME_DP = df.iloc[i]['DP']
        destino = df.iloc[i]['EXTREMIDADE']
        ponto_final = destino
        k += 1
        while True:
            extremidade = ponto_final
            origem = CABLE_FINAL.getFeatures("DESTINO LIKE '"+extremidade+"'")
                    
            for feature in origem:
                if feature["Label"] == None:
                    ponto_final = feature["ORIGEM"]
                    print(ponto_final)
                    print("teste")
                    CABLE_FINAL.changeAttributeValue(feature.id(), idxEdgeId, NAME_DP + '-K' + str(k).zfill(2) )
                    break
                
            TAMANHO-=1
            if TAMANHO <= 0:
                break      
    CABLE_FINAL.setSubsetString("")

    #COPIES
    print('>Copies')
    F_CABLE = prj.mapLayersByName('Feeder Cable')[0]
    #remove info in origin lyr
    for f in F_CABLE.getFeatures():
        F_CABLE.startEditing()
        F_CABLE.deleteFeature(f.id())

    copyFeatures.copyAll(CABLE_FINAL,F_CABLE)

    #EXPORT .TXT INFO
    print('> output.txt File')
    # import required modules
    from qgis.core import QgsVectorLayer, QgsProject

    # specify the path to the layer
    layer = prj.mapLayersByName('Feeder Cable')[0]

    # specify the path to the output text file
    project_path = prj.readPath("./")
    output_path = project_path + "/Feeder_Cables_output.txt"

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

    print('========================================')
    print("--- END in %s seconds ---" % (time.time() - start_time))
    print('========================================')