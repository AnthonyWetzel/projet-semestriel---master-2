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

    features = []
    for coordonnee in coordLines:
        x_res,y_res = dst(coordonnee[0], coordonnee[1], coordonnee[2], coordonnee[3])
        point = QgsPoint(coordonnee[1], coordonnee[0])
        point2 = QgsPoint(y_res,x_res)
        # Add a new feature and assign the geometry
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolyline([point, point2]))
        features.append(feat)		
    prov_line.addFeatures(features)

    # Update extent of the layer
    layer_line.updateExtents()	 
    # Add the layer to the Layers panel
    QgsProject.instance().addMapLayers([layer_line])

def createLayerPoints(coordPoint):
    """Création d'un layer composé de points"""
    clearLayer('batLayer')
    layer_point = QgsVectorLayer('Point?crs=epsg:4230', 'batLayer', 'memory')
    prov_point = layer_point.dataProvider()

    for point in coordPoint:
        inX = point[0]
        inY = point[1]
        feat_point = QgsFeature()
        geom_point = buildGeomPoint(inX, inY)
        feat_point.setGeometry(geom_point)
        prov_point.addFeatures([feat_point])

    layer_point.updateExtents()
    QgsProject.instance().addMapLayers([layer_point])

def clearLayer(layer):
    """Suppression d'un layer (clear)"""
    layers = QgsProject.instance().mapLayersByName(layer)
    QgsProject.instance().removeMapLayers([layer.id() for layer in layers])