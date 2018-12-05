# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import *
<<<<<<< HEAD:BatPlugin/createLayers.py
from algorithmNewPoint import *
from clearLayers import *
=======
from .algorithmNewPoint import *
>>>>>>> f91ca06e87d305c1fe37a5f81d67bb4b887ba86d:BatPlugin/createLine.py

def createLines(coordLines):
	clearLinesLayer()
	# Specify the geometry type
	layer_line = QgsVectorLayer('LineString?crs=epsg:4230','lineLayer','memory')

	prov_line = layer_line.dataProvider()

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
