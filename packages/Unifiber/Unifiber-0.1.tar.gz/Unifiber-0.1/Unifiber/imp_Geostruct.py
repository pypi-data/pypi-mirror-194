import os,sys
from qgis.core import *
import processing
import time
#tools
scriptpath = "C:\\Byon\Scripts\\unifiber"
sys.path.append(scriptpath)
import tools
#create instance
copyFeatures = tools.CopyFeatures(iface)



""" log
v2.2=added "export-AP" lyr
v2.1=tools.QA, bug fixes
v2.0=tools sync
v1.7=added tools functions, other modifications
v1.6=bug fixes
v1.5=cable labels in a separate script
v1.4.1=bug fixes
v1.4=cable lables info
v1.3=added fix geometries
v1.2=added DHH equipm
v1.1=fixed some bugs, changed Join fields
v1.0=first dev version (missing export)
"""

def imp_Geostruct():

    #0.0 DEFINITIONS
    prj = QgsProject.instance()
    prjTitle = prj.title()
    root = prj.layerTreeRoot()
    start_time = time.time()    #Timer

    progression = 0 #index management
    """0=import / 1=layers / 2=fix geometries / 3=joins / 4=copies / 5=export"""

    #0. set directories structure
    prj_path = prj.readPath("./")
    qgis_layers_path = prj_path + "/Shapes de Base"
    export_layers_path = prj_path + "/export_shapes/"
    _temp_path = prj_path+"/_temp/"
    #scriptpath = "c:/QGIS/Reference Data/Scripts/"  #DEFINIR CAMINHO

    #0.3 Project Title
    if prjTitle == 'prj_title':
        prjTitle = tools.titleDialog("Title","Insert Value: ","<title>")
    #prj.write(prj_path) #saves the project(optional)

    #0.6 Processing Run
    #def processingRun (name,param):
    #    #name:'string'|param:{dic}
    #    processing.run('native:snapgeometries', {
    #        'BEHAVIOR': 2,  # Prefer aligning nodes, don't insert new vertices
    #        'INPUT': ALL_PT['OUTPUT'],
    #        'REFERENCE_LAYER': export_paal_lyr,
    #        'TOLERANCE': 0.15,
    #        #'OUTPUT': parameters['Snapped_aerialboxes']
    #        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    #    })

    #0.7 Set QA
    tools.resetQALayer(None)
    tools.resetQALayerLn(None)

    # 1.0 LAYERS MANAGEMENT

    ## 1.1 EXPORTED LAYERS FROM GEOSTRUCT TO "export" GROUP
    print('> Imports')
    if progression == 0:
        groupName="export"
        group = root.addGroup(groupName)

        vlyrMap = ["export - A-Cable", "export - A-Duct", "export - A-Area", "export - Aerial Box",
                    "export - Aerial Duct", "export - Aerial Route", "export - BE",
                    "export - CO", "export - AP", "export - D-Cable", "export - D-Duct", "export - HLDDuct",
                    "export - D-HH", "export - DP", "export - Drop Cable", "export - Façade Route",
                    "export - HP", "export - F-Cable", "export - Paal", "export - Geul", "export - Persing",
                    "export - Riser", "export - Termination Box", "export - Koppeling"]
                    #ADICIONAR O KOEPELING

        #1.1.1 pode ser definida "path" e adicionar cm map loop
            #https://gis.stackexchange.com/questions/290938/adding-layer-to-group-in-layers-panel-using-pyqgis
        for shape in vlyrMap:
            export_layers_path = export_layers_path + shape + ".shp"
            vlayer = QgsVectorLayer(export_layers_path, shape,"ogr")
            prj.addMapLayer(vlayer, False)
            group.addLayer(vlayer)
            
            
            #print(vlayer.name() + ' added')  #debug        
            export_layers_path = prj_path + "/export_shapes/"    #reset path
        
        progression += 1 #jump
    else:
        #progression = progression + 1 #jump
        print('[i1.1] - Import from GeoStruct skipped')

    ## 1.2 DEFINE LAYERS IN PROJECT
    print('> Layers Management')
        #set the layers variable = a list of all the layer objects open in the QGIS interface
    if progression == 1:
        #lyrs
        co_lyr = prj.mapLayersByName('CO')[0]
        dp_lyr = prj.mapLayersByName('DP')[0]
        dhh_lyr = prj.mapLayersByName('DHH')[0]
        riser_lyr = prj.mapLayersByName('Riser')[0]
        poleClosure_lyr = prj.mapLayersByName('Pole Closure')[0]
        facadeClosure_lyr = prj.mapLayersByName('FacadeClosure')[0]
        terminationBox_lyr = prj.mapLayersByName('TerminationBox')[0]
        dropCable_lyr = prj.mapLayersByName('DropCable')[0]
        distCables_lyr = prj.mapLayersByName('Distribution Cables')[0]
        feedCable_lyr = prj.mapLayersByName('Feeder Cable')[0]
        multFus_lyr = prj.mapLayersByName('MultiFus')[0]
        dDucts_lyr = prj.mapLayersByName('D-Ducts')[0]
        db1_lyr = prj.mapLayersByName('DB1')[0]
        db4_lyr = prj.mapLayersByName('DB4')[0]
        db7_lyr = prj.mapLayersByName('DB7')[0]
        be_lyr = prj.mapLayersByName('BE')[0]
        paal_lyr = prj.mapLayersByName('Paal')[0]
        hp_lyr = prj.mapLayersByName('HPs')[0]
        bk_lyr = prj.mapLayersByName('BK')[0]
        #csv
        aerial_enclosures_lyr = prj.mapLayersByName('aerial_enclosures')[0]
        dp_enclosures_lyr = prj.mapLayersByName('dp_enclosures')[0]
        dhh_enclosures_lyr = prj.mapLayersByName('dhh_enclosures')[0]

        layers = prj.mapLayers().values()
        valid_exp_lrys = []
        for layer in layers:
            #print(layer.name()) #debug
            #export
            if layer.name() == "export - CO" and layer.isValid():
                export_co_lyr = layer
                valid_exp_lrys.append(export_co_lyr)
            if layer.name() == "export - AP" and layer.isValid():
                export_ap_lyr = layer
                valid_exp_lrys.append(export_ap_lyr)
            if layer.name() == "export - DP" and layer.isValid():
                export_dp_lyr = layer
                valid_exp_lrys.append(export_dp_lyr)
            if layer.name() == "export - D-HH" and layer.isValid():
                export_dhh_lyr = layer
                valid_exp_lrys.append(export_dhh_lyr)
            if layer.name() == "export - Riser" and layer.isValid():
                export_riser_lyr = layer
                valid_exp_lrys.append(export_riser_lyr)
            if layer.name() == "export - Aerial Box" and layer.isValid():
                export_ab_lyr = layer
                valid_exp_lrys.append(export_ab_lyr)
            if layer.name() == "export - Termination Box" and layer.isValid():
                export_terminationBox_lyr = layer
                valid_exp_lrys.append(export_terminationBox_lyr)
            if layer.name() == "export - A-Cable" and layer.isValid():  #dropCables
                export_aCable_lyr = layer
                valid_exp_lrys.append(export_aCable_lyr)
            if layer.name() == "export - A-Area" and layer.isValid():
                export_aArea_lyr = layer
                valid_exp_lrys.append(export_aArea_lyr)
            if layer.name() == "export - D-Cable" and layer.isValid():
                export_dCables_lyr = layer
                valid_exp_lrys.append(export_dCables_lyr)
            if layer.name() == "export - F-Cable" and layer.isValid():
                export_fCable_lyr = layer
                valid_exp_lrys.append(export_fCable_lyr)
            if layer.name() == "export - A-Duct" and layer.isValid():
                export_aDuct_lyr = layer
                valid_exp_lrys.append(export_aDuct_lyr)
            if layer.name() == "export - D-Duct" and layer.isValid():
                export_dDucts_lyr = layer
                valid_exp_lrys.append(export_dDucts_lyr)
            if layer.name() == "export - BE" and layer.isValid():
                export_be_lyr = layer
                valid_exp_lrys.append(export_be_lyr)
            if layer.name() == "export - Paal" and layer.isValid():
                export_paal_lyr = layer
                valid_exp_lrys.append(export_paal_lyr)
            if layer.name() == "export - HP" and layer.isValid():
                export_hp_lyr = layer
                valid_exp_lrys.append(export_hp_lyr)
            if layer.name() == "export - HLDDuct" and layer.isValid():
                export_hldD_lyr = layer
                valid_exp_lrys.append(export_hldD_lyr)
            if layer.name() == "export - Koppeling" and layer.isValid():
                export_bk_lyr = layer
                valid_exp_lrys.append(export_bk_lyr)
        
        p_list =[]
        filter = ["export - DP","export - Riser","export - Aerial Box","export - Termination Box","export - CO","export - AP","export - D-HH","export - BE","export - HP","export - Koppeling"]
        for i in valid_exp_lrys:
            for p in filter:
                if i.name() == p:
                    p_list.append(i)
        #print(p_list)

        l_list = []
        filter = ["export - A-Cable", "export - A-Duct", "export - F-Cable", "export - D-Duct"]
        for i in valid_exp_lrys:
            for l in filter:
                if i.name() == l:
                    l_list.append(i)
        #print(p_list)
        progression += 1 #jump
    else:
        #progression = progression + 1 #jump
        print('[i1.2] - Layers Defnition skipped')

    ## 1.3 FIX GEOMETRIES
    print('> Fix Geometries')
    if progression == 2:    
        _temp_groupName="_temp"
        _tempGroup = root.addGroup(_temp_groupName)

        #processing calfunctions
        #JUNTA TODOS OS PONTOS
        ALL_PT = processing.run("native:mergevectorlayers", 
        #{'LAYERS':[export_dp_lyr, export_riser_lyr, export_ab_lyr, export_terminationBox_lyr, export_co_lyr, export_dhh_lyr, export_be_lyr, export_hp_lyr, export_bk_lyr],
        {'LAYERS':p_list,
        'CRS':QgsCoordinateReferenceSystem('EPSG:31370'),
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})
        
        SNAP_PONTOS = processing.run('native:snapgeometries', {
            'BEHAVIOR': 2,  # Prefer aligning nodes, don't insert new vertices
            'INPUT': ALL_PT['OUTPUT'],
            'REFERENCE_LAYER': export_paal_lyr,
            'TOLERANCE': 0.15,
            #'OUTPUT': parameters['Snapped_aerialboxes']
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        })

        #ATUALIZA O CAMPO ID
        ALL_PT = processing.run("native:fieldcalculator", 
        {'INPUT':SNAP_PONTOS['OUTPUT'],
        'FIELD_NAME':'ID',
        'FIELD_TYPE':2,
        'FIELD_LENGTH':250,
        'FIELD_PRECISION':0,
        'FORMULA':"$ID",
        'OUTPUT':_temp_path+'Points_Final.shp'
        }) #########################
        vlayer = QgsVectorLayer(_temp_path+'Points_Final.shp', 'Points_Final', "ogr")
        prj.addMapLayer(vlayer, False)
        _tempGroup.addLayer(vlayer)

        for i in valid_exp_lrys:
            if i.name() == "export - D-Cable":
                #FIX AS (dist) CABLES AOS ALL_PT
                DIST_CABLES = processing.run("native:fixgeometries", 
                {'INPUT':export_dCables_lyr,
                'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT})

                #ATRAI AS (dist) CABLES AOS ALL_PT
                DIST_CABLES = processing.run("native:snapgeometries", 
                {'INPUT':DIST_CABLES['OUTPUT'],
                'REFERENCE_LAYER':ALL_PT['OUTPUT'],
                'TOLERANCE':0.2,
                'BEHAVIOR':0,
                'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT})

                #CAMPOS DE ORIGEM E DESTINO
                DIST_CABLES = processing.run("native:fieldcalculator", 
                {'INPUT':DIST_CABLES['OUTPUT'],
                'FIELD_NAME':'ORIGEM',
                'FIELD_TYPE':2,
                'FIELD_LENGTH':250,
                'FIELD_PRECISION':0,
                'FORMULA':"aggregate(\r\nlayer:= 'Points_Final',\r\naggregate:='concatenate',\r\nexpression:= to_string(ID),\r\nconcatenator:=',',\r\nfilter:=intersects($geometry, start_point(geometry(@parent))))\r\n",'OUTPUT':'TEMPORARY_OUTPUT'})

                DIST_CABLES = processing.run("native:fieldcalculator", 
                {'INPUT':DIST_CABLES['OUTPUT'],
                'FIELD_NAME':'DESTINO',
                'FIELD_TYPE':2,
                'FIELD_LENGTH':250,
                'FIELD_PRECISION':0,
                'FORMULA':"aggregate(\r\nlayer:= 'Points_Final',\r\naggregate:='concatenate',\r\nexpression:= to_string(ID),\r\nconcatenator:=',',\r\nfilter:=intersects($geometry, end_point(geometry(@parent))))\r\n",'OUTPUT':'TEMPORARY_OUTPUT'})

                DIST_CABLES = processing.run("native:addfieldtoattributestable", 
                {'INPUT':DIST_CABLES['OUTPUT'],
                'FIELD_NAME':'Label',
                'FIELD_TYPE':2,
                'FIELD_LENGTH':150,
                'FIELD_PRECISION':0,
                'OUTPUT':_temp_path+'Cable_Dist.shp'
                }) #########################
                vlayer = QgsVectorLayer(_temp_path+'Cable_Dist.shp', 'Cable_Dist', "ogr")
                prj.addMapLayer(vlayer, False)
                _tempGroup.addLayer(vlayer)

        #ADICIONA (others) CABLES AOS ALL_PT
        OTHR_CABLES = processing.run("native:mergevectorlayers", 
        {'LAYERS':l_list,
        'CRS':QgsCoordinateReferenceSystem('EPSG:31370'),
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})

        OTHR_CABLES = processing.run("native:fixgeometries", 
        {'INPUT':OTHR_CABLES['OUTPUT'],
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT})

        OTHR_CABLES = processing.run("native:snapgeometries", 
        {'INPUT':OTHR_CABLES['OUTPUT'],
        'REFERENCE_LAYER':ALL_PT['OUTPUT'],
        'TOLERANCE':0.2,
        'BEHAVIOR':0,
        'OUTPUT':_temp_path+'Cable_others.shp'
        }) #########################
        vlayer = QgsVectorLayer(_temp_path+'Cable_others.shp', 'Cable_others', "ogr")
        prj.addMapLayer(vlayer, False)
        _tempGroup.addLayer(vlayer)

        _temp_othrCable_lyr = prj.mapLayersByName('Cable_others')[0]
        _temp_points_lyr = prj.mapLayersByName('Points_Final')[0]
        try:
            _temp_distCable_lyr = prj.mapLayersByName('Cable_Dist')[0]
            tools.check_dCables_length(_temp_distCable_lyr,'GeoLength')
            tools.check_dCables(_temp_distCable_lyr,'Points_Final')
        except:
            print('     [ERROR] Missing d-Cables')
        progression += 1 #jump
    else:
        #progression = progression + 1 #jump
        print('[i1.3] - Fix Geometries skipped')

    ## 1.4 CREATE JOIN IN LAYER
    print('> Join Layers')
        #gis.stackexchange.com/questions/133573/joining-table-field-with-shapefile-using-pyqgis
        #gis.stackexchange.com/questions/267732/joining-layers-with-pyqgis-3
    if progression == 3:

        ### 1.4.1 remove info in origin lyrs
        toRemove = [export_ab_lyr, export_dp_lyr, export_dhh_lyr]
        for f_lyr in toRemove:
            for f in f_lyr.getFeatures():
                f_lyr.startEditing()
                f_lyr.deleteFeature(f.id())

        ### 1.4.2 GET INFO
        #ab
        copyFeatures.copyByExp(_temp_points_lyr,export_ab_lyr,'\"layer\"= \'export - Aerial Box\'')
        #tools.ClearSelection()

        #DP
        copyFeatures.copyByExp(_temp_points_lyr,export_dp_lyr,'\"layer\"= \'export - DP\'')
        #tools.ClearSelection()
        
        #D-HH
        copyFeatures.copyByExp(_temp_points_lyr,export_dhh_lyr,'\"layer\"= \'export - D-HH\'')
        tools.ClearSelection()

        ### 1.4.3 Get input (csv) and target (Shapefile) layers
        #shp=iface.activeLayer()
        #csv=iface.mapCanvas().layers()[0] #VER INDICE DO CAMPO OU TALVEZ BUSCAR POR NOME
        csvFiles = ["aerial_enclosures", "dhh_enclosures", "dp_enclosures"]
        joinTargets = ["export - DP", "export - Aerial Box"]
        joinList = [["aerial_enclosures", "dhh_enclosures", "dp_enclosures"], 
                    ["export - DP", "export - Aerial Box"]] #[0]lyr - [1]target

        ### 1.4.4 Set properties for the join
        #DP
        shpField='Label'
        csvField='Label'
        joinObject = QgsVectorLayerJoinInfo()

        joinObject.setJoinFieldName(csvField)
        joinObject.setTargetFieldName(shpField)
        joinObject.setJoinLayerId(dp_enclosures_lyr.id())
        joinObject.setUsingMemoryCache(True)
        joinObject.setJoinLayer(dp_enclosures_lyr)
        export_dp_lyr.addJoin(joinObject)
        #check invalid joins
        tools.check_enclosures(export_dp_lyr,'dp_enclosures_Type','Identifier')

        #AB
        shpField='Label'
        csvField='Label'
        joinObject = QgsVectorLayerJoinInfo()

        joinObject.setJoinFieldName(csvField)
        joinObject.setTargetFieldName(shpField)
        joinObject.setJoinLayerId(aerial_enclosures_lyr.id())
        joinObject.setUsingMemoryCache(True)
        joinObject.setJoinLayer(aerial_enclosures_lyr)
        export_ab_lyr.addJoin(joinObject)
        #check invalid joins
        tools.check_enclosures(export_ab_lyr,'ab_enclosures_Type','Label')

        #DHH
        shpField='Label'
        csvField='Label'
        joinObject = QgsVectorLayerJoinInfo()

        joinObject.setJoinFieldName(csvField)
        joinObject.setTargetFieldName(shpField)
        joinObject.setJoinLayerId(dhh_enclosures_lyr.id())
        joinObject.setUsingMemoryCache(True)
        joinObject.setJoinLayer(dhh_enclosures_lyr)
        export_dhh_lyr.addJoin(joinObject)
        #check invalid joins
        tools.check_enclosures(export_dhh_lyr,'dhh_enclosures_Type','Identifier')

        progression += 1 #jump
    else:
        print('[i1.4] - Join in Layers skipped')

    ## 1.5 COPY INFO FROM EXP LYRS FOR EACH LAYER
    print('> Copies')
        #opensourceoptions.com/blog/pyqgis-select-features-from-a-vector-layer/
    if progression == 4:

        #joint lyrs
        #Pole Closure
        copyFeatures.copyByExp(export_ab_lyr,poleClosure_lyr,'\"aerial_enclosures_Type\"= \'OFDC-A4\' OR \"aerial_enclosures_Type\"= \'OFDC-B8G\'')

        #Facade Closure
        copyFeatures.copyByExp(export_ab_lyr,facadeClosure_lyr,'\"aerial_enclosures_Type\"= \'Novux Closure\'')
        
        #DP
        copyFeatures.copyAll(export_dp_lyr,dp_lyr)
        #update fields
        dp_lyr.startEditing()
        try:
            lb_idx = dp_lyr.fields().lookupField('Label')
        except:
            print('lookupField(\'Label\') doesn\'t exists')

        for f in dp_lyr.getFeatures():
            name = f.attributes()[f.fields().indexFromName('Label')]
            value = prjTitle +'-'+ name

            atts = {lb_idx: value}
            dp_lyr.changeAttributeValues(f.id(), atts)
        dp_lyr.commitChanges()
        dp_lyr = prj.mapLayersByName('DP')[0]     #update value

        #DHH
        copyFeatures.copyAll(export_dhh_lyr,dhh_lyr)
        tools.ClearSelection()

        ############################
    
        #Distribution Cables
        try:
            copyFeatures.copyAll(_temp_distCable_lyr,distCables_lyr)
            tools.ClearSelection()
        except:
            print('     [ERROR] Missing d-Cables')

        ############################

        #Riser
        copyFeatures.copyByExp(_temp_points_lyr,riser_lyr,'\"layer\"= \'export - Riser\'')
        #tools.ClearSelection()

        #D-Ducts
        copyFeatures.copyByExp(_temp_othrCable_lyr,dDucts_lyr,'\"layer\"= \'export - D-Duct\'')
        #tools.ClearSelection()
        copyFeatures.copyByExp(dDucts_lyr,db1_lyr,'\"Type\"= \'1DB\'')
        copyFeatures.copyByExp(dDucts_lyr,db4_lyr,'\"Type\"= \'4DB\'')
        copyFeatures.copyByExp(dDucts_lyr,db7_lyr,'\"Type\"= \'7DB\'')

        #Drop Cables
        copyFeatures.copyByExp(_temp_othrCable_lyr,dropCable_lyr,'\"layer\"= \'export - A-Cable\'')
        #tools.ClearSelection()

        #Paal
        copyFeatures.copyAll(export_paal_lyr,paal_lyr)
        #tools.ClearSelection()

        #Multifus
        copyFeatures.copyByExp(_temp_othrCable_lyr,multFus_lyr,'\"layer\"= \'export - A-Duct\'')
        #tools.ClearSelection()

        #CO
        copyFeatures.copyByExp(_temp_points_lyr,co_lyr,'\"layer\"= \'export - CO\'')
        copyFeatures.copyByExp(_temp_points_lyr,co_lyr,'\"layer\"= \'export - AP\'')
        #tools.ClearSelection()

        #BE
        copyFeatures.copyByExp(_temp_points_lyr,be_lyr,'\"layer\"= \'export - BE\'')
        #tools.ClearSelection()

        #Termination Box
        copyFeatures.copyByExp(_temp_points_lyr,terminationBox_lyr,'\"layer\"= \'export - Termination Box\'')
        #tools.ClearSelection()

        #fCable
        copyFeatures.copyByExp(_temp_othrCable_lyr,feedCable_lyr,'\"layer\"= \'export - F-Cable\'')
        #tools.ClearSelection()

        #HP
        copyFeatures.copyByExp(_temp_points_lyr,hp_lyr,'\"layer\"= \'export - HP\'')
        #tools.ClearSelection()

        #BK
        copyFeatures.copyByExp(_temp_points_lyr,bk_lyr,'\"layer\"= \'export - Koppeling\'')
        tools.ClearSelection()

        progression += 1 #jump
    else:
        print('[i1.5] - Layer Copies skipped')


    iface.messageBar().clearWidgets()

    print('========================================')
    print("--- END in %s seconds ---" % (time.time() - start_time))
    print('========================================')