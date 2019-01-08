# -*- coding: utf-8 -*
from qgis.utils import iface
from qgis.core import QgsVectorLayer, QgsFeature, QgsPoint, QgsGeometry
from .algorithmNewPoint import dst
from .compat2qgis import QgsProject
from .compat2qgis import buildGeomPoint

def createLayerLines(coordLines):
    """Création d'un layer composé de lignes"""
    clearLayer('lineLayer')
    # Specify the geometry type
    layer_line = QgsVectorLayer('LineString?crs=epsg:4230', 'lineLayer', 'memory')
    prov_line = layer_line.dataProvider()
    # Create and add line features
    features = []
    for coordonnee in coordLines:
        x_res,y_res = dst(coordonnee[0], coordonnee[1], coordonnee[2], coordonnee[3])
        point = QgsPoint(coordonnee[1], coordonnee[0])
        point2 = QgsPoint(y_res,x_res)
        # Add a new feature and assign the geometry
        feat_line = QgsFeature()
        feat_line.setGeometry(QgsGeometry.fromPolyline([point, point2]))
        features.append(feat_line)		
    prov_line.addFeatures(features)

    # Update extent of the layer
    layer_line.updateExtents()	 
    # Add the layer to the Layers panel
    QgsProject.instance().addMapLayers([layer_line])

def createLayerPoints(coordPoints):
    """Création d'un layer composé de points"""
    clearLayer('batLayer')
    # Specify the geometry type
    layer_point = QgsVectorLayer('Point?crs=epsg:4230', 'batLayer', 'memory')
    prov_point = layer_point.dataProvider()
    # Create and add point features
    features = []
    for point in coordPoints:
        inX = point[0]
        inY = point[1]
        # Add a new feature and assign the geometry
        feat_point = QgsFeature()
        feat_point.setGeometry(buildGeomPoint(inX, inY))
        features.append(feat_point)
    prov_point.addFeatures(features)

    # Update extent of the layer
    layer_point.updateExtents()
    # Add the layer to the Layers panel
    QgsProject.instance().addMapLayers([layer_point])

def clearLayer(layer):
    """Suppression d'un layer (clear)"""
    layers = QgsProject.instance().mapLayersByName(layer)
    QgsProject.instance().removeMapLayers([layer.id() for layer in layers])