# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
from algorithmNewPoint import *
"""
def createFeatList():
	# Récupérer les données du csv (latitude,longitude,azimut,distance=puissance_signal+filtre_signal)

	# Créer une liste 'l1' avec les données du csv

	# Créer une liste 'l2' en utilisant l'algorithme et les données de la liste 'l1'

	# Retourne les 2 listes
"""

def createLine(feat_list,x_col,y_col):
	# Remove Point and Line layers
	legend = iface.legendInterface()
	layers = legend.layers()
	for layer in layers:
		if layer.name() == 'line':
			QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )

	# Specify the geometry type
	layer = QgsVectorLayer('LineString?crs=epsg:4326','line','memory')
	 
	# Set the provider to accept the data source
	prov = layer.dataProvider()

	features = []

	for feature in feat_list:
		x_coord = feature[x_col]
		y_coord = feature[y_col]

		x_res,y_res = dst(x_coord,y_coord,float(feature['azimut']),float(feature['puissance_signal'])+float(feature['niveau_filtre']))

		point = QgsPoint(y_coord,x_coord)
		point2 = QgsPoint(y_res,x_res)

		# Add a new feature and assign the geometry
		feat = QgsFeature()
		feat.setGeometry(QgsGeometry.fromPolyline([point, point2]))
		features.add(feat)		

	prov.addFeatures(features)

	# Update extent of the layer
	layer.updateExtents()
	 
	# Add the layer to the Layers panel
	QgsMapLayerRegistry.instance().addMapLayers([layer])

def createLine2(latitude,longitude):
	# Remove Point and Line layers
	legend = iface.legendInterface()
	layers = legend.layers()
	for layer in layers:
		if layer.name() == 'line':
			QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )

	# Specify the geometry type
	layer = QgsVectorLayer('LineString?crs=epsg:4326','line','memory')
	 
	# Set the provider to accept the data source
	prov = layer.dataProvider()
	point = QgsPoint(5.46573,46.59103)
	point2 = QgsPoint(longitude,latitude)
	 
	# Add a new feature and assign the geometry
	feat = QgsFeature()
	feat.setGeometry(QgsGeometry.fromPolyline([point, point2]))
	prov.addFeatures([feat])

	# Update extent of the layer
	layer.updateExtents()

	# Add the layer to the Layers panel
	QgsMapLayerRegistry.instance().addMapLayers([layer])
