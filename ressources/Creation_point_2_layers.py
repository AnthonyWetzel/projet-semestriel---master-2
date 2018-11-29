# Remove Point and Line layers

legend = iface.legendInterface()
layers = legend.layers()
for layer in layers:
	if layer.name() == 'point' or layer.name() == 'line':
		QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )

# Specify the geometry type

layer_point = QgsVectorLayer('Point?crs=epsg:4326', 'point' , 'memory')
layer_line = QgsVectorLayer('LineString?crs=epsg:4326', 'line' , 'memory')

# Set the provider to accept the data source
prov_point = layer_point.dataProvider()
prov_line = layer_line.dataProvider()
point = QgsPoint(5.46573,46.59103)
point2 = QgsPoint(5.4457,46.5976)
 
# Add a new feature and assign the geometry
feat_point = QgsFeature()
feat_point2 = QgsFeature()
feat_line = QgsFeature()

feat_point.setGeometry(QgsGeometry.fromPoint(point))
feat_point2.setGeometry(QgsGeometry.fromPoint(point2))
feat_line.setGeometry(QgsGeometry.fromPolyline([point, point2]))
prov_line.addFeatures([feat_line])
prov_point.addFeatures([feat_point,feat_point2])
 
# Update extent of the layer
layer_point.updateExtents()
layer_line.updateExtents()
 
# Add the layer to the Layers panel
QgsMapLayerRegistry.instance().addMapLayers([layer_line])
QgsMapLayerRegistry.instance().addMapLayers([layer_point])

print('Done')