# Remove Point and Line layers

legend = iface.legendInterface()
layers = legend.layers()
for layer in layers:
	if layer.name() == 'point' or layer.name() == 'line' or layer.name() == 'point2':
		QgsMapLayerRegistry.instance().removeMapLayers( [layer.id()] )

# Specify the geometry type
layer = QgsVectorLayer('Point?crs=epsg:4326', 'point' , 'memory')
layer2 = QgsVectorLayer('Point?crs=epsg:4326', 'point2' , 'memory')
layer_line = QgsVectorLayer('LineString?crs=epsg:4326', 'line' , 'memory')
 
# Set the provider to accept the data source
prov = layer.dataProvider()
prov2 = layer2.dataProvider()
prov_line = layer_line.dataProvider()
point = QgsPoint(5.46573,46.59103)
point2 = QgsPoint(5.4457,46.5976)
 
# Add a new feature and assign the geometry
feat = QgsFeature()
feat2 = QgsFeature()
feat_line = QgsFeature()
feat.setGeometry(QgsGeometry.fromPoint(point))
feat2.setGeometry(QgsGeometry.fromPoint(point2))
feat_line.setGeometry(QgsGeometry.fromPolyline([point, point2]))
prov.addFeatures([feat])
prov2.addFeatures([feat2])
prov_line.addFeatures([feat_line])
 
# Update extent of the layer
layer.updateExtents()
layer2.updateExtents()
layer_line.updateExtents()
 
# Add the layer to the Layers panel
QgsMapLayerRegistry.instance().addMapLayers([layer])
QgsMapLayerRegistry.instance().addMapLayers([layer2])
QgsMapLayerRegistry.instance().addMapLayers([layer_line])
