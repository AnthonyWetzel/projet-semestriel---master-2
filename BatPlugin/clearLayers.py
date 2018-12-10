# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from .algorithmNewPoint import *
from .compat2qgis import QgsProject

def clearLinesLayer():
        layers = QgsProject.instance().mapLayersByName('lineLayer')
        QgsProject.instance().removeMapLayers([layer.id() for layer in layers])

def clearBatLayer():
        layers = QgsProject.instance().mapLayersByName('batLayer')
        QgsProject.instance().removeMapLayers([layer.id() for layer in layers])
