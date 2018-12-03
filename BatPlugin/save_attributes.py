# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SaveAttributes
                                 A QGIS plugin
 This plugin saves the attribute of the selected vector layer as a CSV file.
                              -------------------
        begin                : 2015-04-20
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Ujaval Gandhi
        email                : ujaval@spatialthoughts.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *

#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
from . import resources
# Import the code for the dialog
#from save_attributes_dialog import SaveAttributesDialog
import os.path


class SaveAttributes:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SaveAttributes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SaveAttributesDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Save Attributes')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SaveAttributes')
        self.toolbar.setObjectName(u'SaveAttributes')
        
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_file)
        self.dlg.comboBox.currentIndexChanged.connect(self.select_entities)

        self.generate_data_table()
        self.dlg.pushButton_2.clicked.connect(self.generate_data_table)
        
        
        self.dlg.lineEdit_2.clear()
        self.dlg.pushButton_3.clicked.connect(self.getfiles)
  

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SaveAttributes', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SaveAttributes/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Save Attributes as CSV'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Save Attributes'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.csv')
        self.dlg.lineEdit.setText(filename+'.csv')
    
    def select_entities(self):
        self.dlg.comboBox_2.clear()
        try:
            layers = self.iface.legendInterface().layers()
            entity_list = []
            currentLayer = layers[self.dlg.comboBox.currentIndex()].getFeatures()
            for entity in currentLayer:
                entity_list.append(entity['Id_Indiv'])
            self.dlg.comboBox_2.addItems(entity_list)
        except:
            entity_list = []
            entity_list.append('No valid data')
       
            self.dlg.comboBox_2.addItems(entity_list)       
       

    def generate_data_table(self):

        layers = self.iface.legendInterface().layers()
        try:
            selectedLayer = layers[len(layers)-2]
            fields = selectedLayer.pendingFields()  
            fieldnames = [field.name() for field in fields]

            qTable = self.dlg.tableWidget
            qTable.setRowCount(39)#"""changer pour length"""
            qTable.setColumnCount(9)
            headers = ['Id_indiv','Individu','Date','Coordonnées_WGS84_N','Coordonnées_WGS84_E','azimuœt','niveau_filtre','puissance_signal','Info additionnelle']
            qTable.setHorizontalHeaderLabels(headers)
            qTable.resizeColumnsToContents()
            qTable.resizeRowsToContents()
            n = 0
            for key in selectedLayer.getFeatures():
                m = 0
                for item in fieldnames:
                    newitem = QTableWidgetItem(unicode(key[item]))
                    qTable.setItem(n, m, newitem)
                    print(unicode(key[item]))
                    m += 1
                n += 1    
            qTable.resizeColumnsToContents()
            qTable.resizeRowsToContents()
        except:
            print('No layer exists')
        

    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("Text files (*.csv)")
        #filenames = QStringList()
        
        items = []
        contents = []

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')
            
            layer = QgsVectorLayer(filenames,'test','delilitedtext')   
            print(layer) 
            with f:
                data = f.read()
                items.append(data)
                print(items)
            contents.append(items)
            print(contents)
        fields = contents.pendingFields()  
        fieldnames = [field.name() for field in fields]
        print(fieldnames)
        #self.dlg.lineEdit_2.setText(contents)

    def run(self):
        
        """Run method that performs all the real work"""
        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
                layer_list.append(layer.name())       
        self.dlg.comboBox.clear()
        self.dlg.comboBox.addItems(layer_list)
        
        #self.dlg.tableWidget.clear()
        self.dlg.lineEdit.clear()
        #self.dlg.lineEdit_2.setText(self.dlg.comboBox.currentIndex())
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            filename = self.dlg.lineEdit.text()
            output_file = open(filename, 'w')
           
            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            selectedLayer = layers[selectedLayerIndex]
            fields = selectedLayer.pendingFields()
            fieldnames = [field.name() for field in fields]
            
            selFeatures = selectedLayer.selectedFeatures()
            ids = [f.id() for f in selFeatures]
            #print ('id ', ids)
            #for fid in ids:
                #print ( fid )
                


            entities = selectedLayer.getFeatures() 
            selectedEntityIndex = self.dlg.comboBox_2.currentIndex()
            
            #print ('entity ',selectedEntityIndex)
            #print ('layer ',selectedLayerIndex)
            #print fields[selectedLayerIndex].name()
            #for f in fields:
                #print f.name()

            for f in selectedLayer.getFeatures():
                line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
                #print line
                unicode_line = line.encode('utf-8')
                output_file.write(unicode_line)
            output_file.close()

            #for f in selectedLayer.getFeatures():
               #print f['Id_Indiv']
                #print (QgsFeature(f[x].fields().attributes()) for x in fieldnames)
                #print f.attributes
                #line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
                #unicode_line = line.encode('utf-8')
                #output_file.write(unicode_line)
            #output_file.close()
            #for f in selectedLayer.getFeatures():
             #   line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
              #  unicode_line = line.encode('utf-8')
               # output_file.write(unicode_line)
            #output_file.close()

