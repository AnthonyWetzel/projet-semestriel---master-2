# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from .clearLayers import *
from .compat2qgis import buildGeomPoint
from .compat2qgis import addMapLayers

def createPoints(coordPoint):
	clearBatLayer()
	layer_point = QgsVectorLayer('Point?crs=epsg:4230', 'batLayer' , 'memory')
	prov_point = layer_point.dataProvider()

	for point in coordPoint:
		inX = point[0]
		inY = point[1]
		feat_point = QgsFeature()
		geom_point = buildGeomPoint(inX,inY)
		feat_point.setGeometry(geom_point)

		prov_point.addFeatures([feat_point])
		layer_point.updateExtents()
		addMapLayers([layer_point])
