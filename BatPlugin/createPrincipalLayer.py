# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from .clearLayers import *

def createPoints(coordPoint):
	clearBatLayer()
	layer_point = QgsVectorLayer('Point?crs=epsg:4230', 'batLayer' , 'memory')
	prov_point = layer_point.dataProvider()

	for point in coordPoint:
		inX = point[0]
		inY = point[1]
		feat_point = QgsFeature()
		try:
			point = QgsPoint(inX,inY)
			feat_point.setGeometry(QgsGeometry.fromPoint(point))
		except:
			point = QgsPointXY(inX,inY)
			feat_point.setGeometry(QgsGeometry.fromPointXY(point))

		prov_point.addFeatures([feat_point])
		layer_point.updateExtents()
		try:
			QgsMapLayerRegistry.instance().addMapLayers([layer_point])
		except:
			QgsProject.instance().addMapLayers([layer_point])
