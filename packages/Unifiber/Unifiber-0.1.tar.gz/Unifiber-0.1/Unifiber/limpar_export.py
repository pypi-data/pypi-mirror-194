import os,sys
from PyQt5.QtCore import QVariant #FOR MODIFYING LYR ATTRIBUTES
import processing
import time
from qgis.core import *


def limpar():
    start_time = time.time()    #Timer
    export_group = "export"
    temp_group = "_temp"

    root = QgsProject.instance().layerTreeRoot()
    group_layer = root.findGroup(export_group)
    group_layer2 = root.findGroup(temp_group)
    root.removeChildNode(group_layer)
    root.removeChildNode(group_layer2)

    # Get all layers in the project
    layers = QgsProject.instance().mapLayers().values()

    time.sleep(5)
    # Loop over each layer and delete all features
    for layer in layers:
        if layer.name() != "aerial_enclosures" and layer.name()!="dp_enclosures" and layer.name()!="dhh_enclosures":
            with edit(layer):
                layer.deleteFeatures(layer.allFeatureIds())

    print('========================================')
    print("--- END in %s seconds ---" % (time.time() - start_time))
    print('========================================')
    ########################################################