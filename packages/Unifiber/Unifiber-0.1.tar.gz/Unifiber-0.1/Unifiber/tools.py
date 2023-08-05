# -*- coding: utf-8 -*-

"""
**************************STANDALONE SCRIPT********************************
*                                                                         *
*   Used for side processing for UNIFIBER PROJECT Suit.                   *
*                                                                         *
***************************************************************************
"""

#qgs imports
from qgis.core import *
from PyQt5.QtCore import QVariant #for modifing fields values
from PyQt5.QtWidgets import *
from qgis.gui import *
#from qgis.gui import QgsMapCanvas
import os
import processing

def tools(s):
    # DEF
    prj = QgsProject.instance()
    root = prj.layerTreeRoot()
    ##paths
    project_path = prj.readPath("./")


    # PROCESSING ################
    ## UI - ASKING DIALOG
    """expects a title to change Projct Title"""
    def titleDialog(t,l,placeholder):   #t:<str>|l:<str>|placeholder:<str>
        qid = QInputDialog()
        title = t                   #"Title"
        label = l                   #"Insert Value: "
        mode = QLineEdit.Normal
        default = placeholder       #"<title>"
        tit, ok = QInputDialog.getText(qid, title, label, mode, default)
        prj.setTitle(tit)
        prjTitle = prj.title()
        return prjTitle

    ## LAYERS - ADD LYRS IN GROUP(creates new one)
    def addLyrstoGrp(new,groupName,layers,lyrs_path):   #new:<T/F>|groupName:<str>|layers:<arry>|lyrs_path:<str>
        if new == True:
            groupName="Name"
            group = root.addGroup(groupName)     #if group don't exists
        else:
            group = root.findGroup(groupName)   #if group exist
        #layers = ["layer_name1","layer_name2","layer_name3","...","layer_name"]

            #defines path to find storaged layers
            #gis.stackexchange.com/questions/290938/adding-layer-to-group-in-layers-panel-using-pyqgis
        for shape_name in layers:
            lyrs_path = lyrs_path + shape_name + ".shp"
            vlayer = QgsVectorLayer(lyrs_path, shape_name,"ogr")
            prj.addMapLayer(vlayer, False)
            group.addLayer(vlayer)
            #print(vlayer.name() + ' added')  #optional
            lyrs_path = project_path + "/lyrs/"    #resets path

    ## LAYERS - Copy FUNCTIONS
    class CopyFeatures:
        def __init__(self, iface):
            # save reference to the QGIS interface
            self.iface = iface
            
        def copyAll(self,source,target): #src:<lyr>|trg:<lyr>
            source.selectAll()
            self.iface.copySelectionToClipboard(source)

            target.startEditing()
            self.iface.pasteFromClipboard(target)
            target.commitChanges()

        def copyByExp(self,source,target,exp):   #src:<lyr>|trg:<lyr>|exp:'str'
            source.selectByExpression(exp)
            self.iface.copySelectionToClipboard(source)

            target.startEditing()
            self.iface.pasteFromClipboard(target)
            target.commitChanges()

    ## LAYERS - clearSelection FUNCTION
    def ClearSelection():   #void
        canvas = QgsMapCanvas()
        for layer in canvas.layers():
            if isinstance(layer, QgsMapLayer):
                layer.removeSelection()
        canvas.refresh()

    # QA ################
    ## Reset
    def resetQALayer(pProcessName): #resetQALayer(None)
        # Erase the contents of the dpi layer, create it if necessary and add to the project.
        try:
            qalayer = prj.mapLayersByName("QA Issues")[0]
        except IndexError:
            qalayer = QgsVectorLayer('Point?crs=epsg:31370&field=Reason:string(254)', 'QA Issues' ,"memory")
            prj.addMapLayer(qalayer)
            ################ adicionar geometria para identificação visual
        
        qalayer.startEditing()
        for ft in qalayer.getFeatures():
            if pProcessName == None or ft.attributes()[0] == pProcessName:
                qalayer.deleteFeature(ft.id())  
        qalayer.commitChanges()

    def resetQALayerLn(pProcessName):
        # Erase the contents of the QA layer, create it if necessary and add to the project.
        try:
            qalayerln = prj.mapLayersByName("QA Issues Linear")[0]
        except IndexError:
            qalayerln = QgsVectorLayer('LineString?crs=epsg:31370&field=reason:string(254)', 'QA Issues Linear' ,"memory")
            prj.addMapLayer(qalayerln)
            ################ adicionar geometria para identificação visual
        
        qalayerln.startEditing()
        for ft in qalayerln.getFeatures():
            if pProcessName == None or ft.attributes()[0] == pProcessName:
                qalayerln.deleteFeature(ft.id())                
        qalayerln.commitChanges()

    ## Create Errors
    def createErr(feat, errmsg):
        qalayer = prj.mapLayersByName('QA Issues')[0]
        outGeom = QgsFeature()
        outGeom.setGeometry(feat.geometry())
        outGeom.setAttributes([errmsg])
        qalayer.dataProvider().addFeatures([outGeom])

    def createErrLn(feat, errmsg):
        qalayerln = prj.mapLayersByName('QA Issues Linear')[0]
        outGeom = QgsFeature()
        outGeom.setGeometry(feat.geometry())
        outGeom.setAttributes([errmsg])
        qalayerln.dataProvider().addFeatures([outGeom])

    def closeQA():
        print('Issues') #rodar um processamento de buffer para cada ponto/linha dentro do lyr de qa

    ## (import.py) FUNÇAO QUE DETECTA SE ALGUMA LABEL NÃO TEM COINCIDENCIA DENTRO DO JOIN
    def check_enclosures(layer,f_index,idx):    #dp|ab|d-hh / 'field index' / if ab:'Label':'Indentifier'
        #checks if critical fields are filled in
        for f in layer.getFeatures():
            if f.attributes()[f.fields().indexFromName(f_index)] == None:
                createErr(f, "Error: No match found for id#{} | {}".format(f.attributes()[f.fields().indexFromName('ID')],f.attributes()[f.fields().indexFromName(idx)]))

    ## CHECK GEOMETRIES (decidir se a verificação deve ser feita antes ou depois das cópias)
    ### (import.py) verificar se (algum dp foi movido) os <export - D-Cable> nao intersecta com <export - DP>
    def check_dCables(layer_ln,layer_pt):   #layer_ln:<lyr>|layer_pt:'str'
        x=0
        for f in layer_ln.getFeatures(QgsFeatureRequest().setFilterExpression (' intersecting_geom_count(\'{}\')=1 '.format(layer_pt))):
            x+=1
            if x != 0:
                msg = "Error: No conection between Cable (fid #{}) and DP".format(f["ID"])
                createErrLn(f,msg)

    ### (import.py) <export - D-Cable> garantir que nao tenha nenhuma geometria nula
    def check_dCables_length(layer,idx):
        #checks the length field if not null
        for fc in layer.getFeatures():
            if fc.attributes()[fc.fields().indexFromName(idx)] == None or fc.attributes()[fc.fields().indexFromName(idx)] == 0:
                createErrLn(fc,"Cable (fid #{}) has NULL length".format(fc["ID"]))

    ### (####.py) <MultiFus> garantir que nao tenha nenhum trecho acima de 600m
    def check_multf_length(layer,idx):
        for fc in layer.getFeatures():
            if fc.attributes()[fc.fields().indexFromName(idx)] > 600:
                createErrLn(fc,"Multifu (fid #{}) has length over 600m".format(fc["ID"]))