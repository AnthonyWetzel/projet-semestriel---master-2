# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from .algorithmNewPoint import *

def clearLinesLayer():
	try:
            legend = iface.legendInterface()
            layers = legend.layers()
        except:
            layers = [layer for layer in QgsProject.instance().mapLayers().values()]
	for layer in layers:
		if layer.name() == 'lineLayer':
			try:
				QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )
			except:
				QgsProject.instance().removeMapLayers( [layer.id()] )


def clearBatLayer():
	try:
            legend = iface.legendInterface()
            layers = legend.layers()
        except:
            layers = [layer for layer in QgsProject.instance().mapLayers().values()]
	for layer in layers:
		if layer.name() == 'batLayer':
			try:
				QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )
			except:
				QgsProject.instance().removeMapLayers( [layer.id()] )
