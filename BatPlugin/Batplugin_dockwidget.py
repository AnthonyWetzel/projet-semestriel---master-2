# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BatPluginDockWidget
                                 A QGIS plugin
 test
                             -------------------
        begin                : 2018-11-10
        git sha              : $Format:%H$
        copyright            : (C) 2018 by chrwiziCorp
        email                : chrwiziCorp@DotCom
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

import os, csv, sys
from qgis.PyQt import QtCore

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

from .createLine import *
from .algorithmNewPoint import *
from .createPrincipalLayer import *

from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsExpression
try:
    from qgis.PyQt.QtGui import QDockWidget, QTableView
except:
    from qgis.PyQt.QtWidgets import QDockWidget, QTableView

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Batplugin_dockwidget_base.ui'))


class BatPluginDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(BatPluginDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.individus=[]
        #Refence to QGIS interface
        self.ifaceRef=None
        self.counter=0
        self.btnValider.clicked.connect(self.slotAddItemcombo)
        self.comboBox.currentIndexChanged.connect(self.slotLabelChange)
        self.btnRecenter.clicked.connect(self.slotRecenterToSelectedPoints)

        #test
        self.btnSelect1.clicked.connect(self.slotSelect)
        self.btnSelect2.clicked.connect(self.slotDeselect)
	
        self.pushButton_2.clicked.connect(self.generate_data_table)
        self.pushButton_3.clicked.connect(self.getfile)
        self.textEdit.clear()
        self.pushButton_4.clicked.connect(self.save)
        self.pushButton.clicked.connect(self.save_as)
        self.pushButton_5.clicked.connect(self.createLineLayer)
        self.tableView.clicked.connect(self.actionTable)
        self.tableView.setSelectionBehavior(QTableView.SelectRows);

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def slotAddItemcombo(self):
        self.comboBox.clear()
        self.comboBox.addItem("")
        layer=self.ifaceRef.activeLayer()
        features=layer.getFeatures()
        for feature in features:
            self.comboBox.addItem(feature['individu'])

    def slotLabelChange(self):
        self.counter+=1
        self.label_2.setText(str(self.comboBox.currentText()))

        #self.ifaceRef.activeLayer().select(self.comboBox.currentIndex())
        #self.ifaceRef.activeLayer().selectByExpression("individu ="+str(self.comboBox.currentText()))
        layer=self.ifaceRef.activeLayer()
        #layer.selectByExpression("individu ="+str(self.comboBox.currentText()))
        seletedItem=str(self.comboBox.currentText())
        #expression=QgsExpression( " \"individu\" = '{}' ".format(seletedItem))
        exp="individu = '%s'"%str(self.comboBox.currentText())
        #layer.selectByExpression("individu ='%s'"%str(self.comboBox.currentText()))
        layer.selectByExpression(exp)
        #layer.select(self.comboBox.currentIndex())

        """Recentre le zoom sur les éléments sélectionnés"""
    def slotRecenterToSelectedPoints(self):
        layer=self.ifaceRef.activeLayer()
        canvas=self.ifaceRef.mapCanvas()
        canvas.zoomToSelected()


    def setIfaceRef(self,iface):
        self.ifaceRef=iface

    def slotSelect(self):
        layer=self.ifaceRef.activeLayer()
        layer.select(0)

    def slotDeselect(self):
        layer=self.ifaceRef.activeLayer()
        layer.deselect(6)

    #def slotCalculNewPoint(self):
        #layer=self.ifaceRef.activeLayer()
        #createLine(layer.getFeatures(),'coordonnees_wgs84_n','coordonnees_wgs84_e')

    def slotBatLayer(self,coordPoint):
        #layer=self.ifaceRef.activeLayer()
        #print(inX,inY)
        createPoints(coordPoint)
    def slotLineLayer(self,coordLines):
        createLines(coordLines)


    def generate_data_table(self):

        layers = self.ifaceRef.legendInterface().layers()
        try:

            selectedLayer = layers[len(layers)-2]
            fields = selectedLayer.pendingFields()  
            fieldnames = [field.name() for field in fields]

            qTable = self.tableWidget
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
                    m += 1
                n += 1    
            qTable.resizeColumnsToContents()
            qTable.resizeRowsToContents()
        except:
            print('No layer exists')

    def createLineLayer(self):
        try:
            layerLine = []
            for feature in range(self.model.rowCount()):
                #for m in range(1):
                    currentRow = self.model.takeRow(feature)
                    self.model.insertRow(feature,currentRow)
                    x = float(currentRow[3].text())
                    y = float(currentRow[4].text())
                    azimut = float(currentRow[5].text())
                    puissance_signal = float(currentRow[7].text())
                    niveau_filtre = float(currentRow[6].text())
                    layerLine.append([x,y,azimut,puissance_signal,niveau_filtre])
                #print(layerPoints)
            self.slotLineLayer(layerLine)
        except:
            print('Error crating line layer')


    def getfile(self):
        self.model = QtGui.QStandardItemModel(self)
        
        layerPoints = []

        qTable = self.tableView

        headers = ['id_observation','id_individu','date','coordonnees_wgs84_n','coordonnees_wgs84_e','azimut','niveau_filtre','puissance_signal']
 
        self.model.setHorizontalHeaderLabels(headers)

        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        try:
            dlg.setFilter("Text files (*.csv)")
        except:
            dlg.setNameFilter("Text files (*.csv)")
        #filenames = QStringList()

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.textEdit.setText(filenames[0])
            with open(filenames[0], "rb") as fileInput:
                for row in csv.reader(fileInput):  
                    #print(row)  
                    items = [
                        QtGui.QStandardItem(field.decode('utf-8'))
                        for field in row
                    ]
                    self.model.appendRow(items)
            qTable.setModel(self.model)
            qTable.resizeColumnsToContents()
            qTable.resizeRowsToContents()
            #print(self.model.rowCount())
            #print(self.model.columnCount())
            #test = self.model.takeRow(1)
            #self.model.appendRow(test)
            #print(test[3].text())
            #print(test[4].text())
            #print(self.model)
            
            for feature in range(self.model.rowCount()):
            #for m in range(1):
                currentRow = self.model.takeRow(feature)
                self.model.insertRow(feature,currentRow)
                #print(test[3].text())
                #print(test[4].text())
                x = float(currentRow[3].text())
                y = float(currentRow[4].text())
                layerPoints.append([y,x])
            #print(layerPoints)
            self.slotBatLayer(layerPoints)

    def save(self):
        try:
            fileName = self.textEdit.toPlainText()
            output_file = open(fileName, 'w')

            with open(fileName, "wb") as fileOutput:
                writer = csv.writer(fileOutput)        
                for feature in range(self.model.rowCount()):
                    aux = []
                    currentRow = self.model.takeRow(feature)
                    self.model.insertRow(feature,currentRow)
                    for n in range(self.model.columnCount()):
                        aux.append((currentRow[n].text()).encode('utf-8').strip())
                    line = ','.join(aux) + '\n'
                    #print('line',line)
                    unicode_line = line
                    output_file.write(unicode_line)
                output_file.close()
            print('File already saved')
        except: 
            print('Error saving file')

    def save_as(self):
        try:
            filename = QFileDialog.getSaveFileName(self, "Select output file ","", '*.csv')
            self.textEdit.setText(filename+'.csv')
            self.save()
        except:
            print('Error saving file')

    def actionTable(self):
        #print('tableView ',self.tableView)
        self.tableView.setSelectionBehavior(QTableView.SelectRows);
        xx = self.tableView.selectedIndexes()
        #print('index ',xx)
        #print('index 0',xx[0])
        #print(xx[0][0])