# -*- coding: utf-8 -*

def createAzimutLayer(features):
	# Specify the geometry type
	layer = QgsVectorLayer('Point?crs=epsg:4326', 'point' , 'memory')
	
	# Set the provider to accept the data source
	prov = layer.dataProvider()

	# Add a new feature and assign the geometry
	feat = QgsFeature()

	listOfPoint=[]
	
