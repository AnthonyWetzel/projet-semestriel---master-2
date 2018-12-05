# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from clearLayers import *

def createPoints(coordPoint):
	clearBatLayer()
	# Specify the geometry type
	layer_point = QgsVectorLayer('Point?crs=epsg:4230', 'batLayer' , 'memory')

	prov_point = layer_point.dataProvider()

	for point in coordPoint:
		inX = point[0]
		inY = point[1]
		point = QgsPoint(inX,inY)
		feat_point = QgsFeature()
		feat_point.setGeometry(QgsGeometry.fromPoint(point))
		prov_point.addFeatures([feat_point])
		layer_point.updateExtents()
		QgsMapLayerRegistry.instance().addMapLayers([layer_point])