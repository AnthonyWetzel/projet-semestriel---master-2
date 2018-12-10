# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from .algorithmNewPoint import *
from .compat2qgis import QgsProject

def clearLinesLayer():
	layers = [layer for layer in QgsProject.instance().mapLayers().values()]
	for layer in layers:
		if layer.name() == 'lineLayer':
			QgsProject.instance().removeMapLayers( [layer.id()] )


def clearBatLayer():
	layers = [layer for layer in QgsProject.instance().mapLayers().values()]
	for layer in layers:
		if layer.name() == 'batLayer':
			QgsProject.instance().removeMapLayers( [layer.id()] )
