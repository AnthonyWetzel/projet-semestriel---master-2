# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from algorithmNewPoint import *

def clearLinesLayer():
	legend = iface.legendInterface()
	layers = legend.layers()
	for layer in layers:
		if layer.name() == 'lineLayer':
			QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )

def clearBatLayer():
	legend = iface.legendInterface()
	layers = legend.layers()
	for layer in layers:
		if layer.name() == 'batLayer':
			QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )