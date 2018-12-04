# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from .algorithmNewPoint import *

def createLines(coordLines):
	legend = iface.legendInterface()
	layers = legend.layers()
	for layer in layers:
		if layer.name() == 'lineLayer':
			QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )

	# Specify the geometry type
	layer_line = QgsVectorLayer('LineString?crs=epsg:4230','lineLayer','memory')

	prov_line = layer_line.dataProvider()

	print('Coordones : ',coordLines)
	print(len(coordLines))

	features = []
	for coordonnee in coordLines:
		x_res,y_res = dst(coordonnee[0],coordonnee[1],coordonnee[2],coordonnee[3]+coordonnee[4])

		point = QgsPoint(coordonnee[1],coordonnee[0])
		point2 = QgsPoint(y_res,x_res)

		# Add a new feature and assign the geometry
		feat = QgsFeature()
		feat.setGeometry(QgsGeometry.fromPolyline([point, point2]))
		features.append(feat)		

	prov_line.addFeatures(features)

	# Update extent of the layer
	layer_line.updateExtents()
	 
	# Add the layer to the Layers panel
	QgsMapLayerRegistry.instance().addMapLayers([layer_line])

	#for point in coordLine:
		#inX = point[0]
		#inY = point[1]
		#print(inX,inY)
		#point = QgsPoint(inX,inY)
		#feat_point = QgsFeature()
		#feat_point.setGeometry(QgsGeometry.fromPoint(point))
		#prov_point.addFeatures([feat_point])
		#layer_point.updateExtents()
		#QgsMapLayerRegistry.instance().addMapLayers([layer_point])