# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *

def createPoint(pointList):
	legend = iface.legendInterface()
	layers = legend.layers()
	for layer in layers:
		if layer.name() == 'batLayer':
			QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )

	layer_point = QgsVectorLayer('Point?crs=epsg:4230', 'batLayer' , 'memory')

	prov_point = layer_point.dataProvider()
	print(pointList)

	for point in pointList:
		inX = point[0]
		inY = point[1]
		#print(inX,inY)
		point = QgsPoint(inX,inY)
		feat_point = QgsFeature()
		feat_point.setGeometry(QgsGeometry.fromPoint(point))
		prov_point.addFeatures([feat_point])
		layer_point.updateExtents()
		QgsMapLayerRegistry.instance().addMapLayers([layer_point])