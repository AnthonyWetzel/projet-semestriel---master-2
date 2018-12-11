# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from .compat2qgis import QgsProject

def clearLayer(layer):
        layers = QgsProject.instance().mapLayersByName(layer)
        QgsProject.instance().removeMapLayers([layer.id() for layer in layers])