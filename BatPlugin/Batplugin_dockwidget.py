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

from createLineLayer import *
from algorithmNewPoint import *
from createPrincipalLayer import *

from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsExpression
from clearLayers import *

try:
    from qgis.PyQt.QtGui import QDockWidget
except:
    from qgis.PyQt.QtWidgets import QDockWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Batplugin_dockwidget_base.ui'))

"""Global variables """
ONE_KM = 12
PAS = 0.1
INDX_ID_OBS = 0
INDX_ID_INDV = 1
INDX_NOM_INDV = 2
INDX_DATE = 3
INDX_X = 4
INDX_Y = 5
INDX_AZMT = 6
INDX_NIV_FILT = 7
INDX_SIGN = 8
INDX_COMM = 9
HEADERS = ['id_observation','id_individu','nom_individu','date','coordonnees_wgs84_n',
                    'coordonnees_wgs84_e','azimut','niveau_filtre','puissance_signal','commentaire']

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
        #self.ifaceRef=None
        
        #Not used statements
        #self.individus=[]
        #self.counter=0
        #self.btnValider.clicked.connect(self.slotAddItemcombo)
        #self.comboBox.currentIndexChanged.connect(self.slotLabelChange)
        #self.btnRecenter.clicked.connect(self.slotRecenterToSelectedPoints)
        #self.btnSelect1.clicked.connect(self.slotSelect)
        #self.btnSelect2.clicked.connect(self.slotDeselect)
        
        """Used statements
            Plugin actions"""
        
        """Clear old layers"""
        clearLinesLayer()
        clearBatLayer()
        """Import and export csv project actions"""
        self.importButton.clicked.connect(self.initializeBatLayer) 
        self.currentProjectText.clear()
        self.saveButton.clicked.connect(self.save)
        self.saveAsButton.clicked.connect(self.save_as)
        
        """Calculation and creation layer observations"""
        self.execLineLayerBtn.clicked.connect(self.createLineLayer)
        
        """Refresh project in table"""
        self.refreshButton.clicked.connect(self.refresh)

        """Table actions"""
        self.tableView.setSelectionBehavior(QTableView.SelectRows);
        

    """Functions to check"""
    """
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

        ""Recentre le zoom sur les éléments sélectionnés""
    def slotRecenterToSelectedPoints(self):
        layer=self.ifaceRef.activeLayer()
        canvas=self.ifaceRef.mapCanvas()
        canvas.zoomToSelected()


    def slotSelect(self):
        layer=self.ifaceRef.activeLayer()
        layer.select(0)

    def slotDeselect(self):
        layer=self.ifaceRef.activeLayer()
        layer.deselect(6)

    def setIfaceRef(self,iface):
        self.ifaceRef=iface

    """

    """Checked Plugin Functions """

    """Refresh current project after modifications"""
    def refresh(self):
        self.save()
        fileName = self.currentProjectText.toPlainText()
        self.createTable(fileName)
        self.createBatLayer()
        clearLinesLayer()

    """Color the rows that have errors"""
    def color(self,row_indx_fail):
        for col in range(self.model.columnCount()):
            for i in range(len(row_indx_fail)):
               self.model.setData(self.model.index(row_indx_fail[i], col), QBrush(Qt.red), QtCore.Qt.BackgroundRole)

    """Create the observations layer from the imported csv file"""
    def createBatLayer(self):
        coordPoint = [] # List of coordinates X,Y to add to the map
        row_indx_fail = 0 
        row_fails = [] #List of rows with errors at the coordinates X and Y
        for feature in range(self.model.rowCount()):
                currentRow = self.model.takeRow(feature)
                self.model.insertRow(feature,currentRow)
                try:
                    coord_x = float(currentRow[INDX_X].text())
                    coord_y = float(currentRow[INDX_Y].text())
                    coordPoint.append([coord_y,coord_x])
                except:
                    print('Fatal error creating BatLayer - Coordinates fatal error at line ',row_indx_fail+1)
                    row_fails.append(row_indx_fail)
                row_indx_fail += 1
        self.color(row_fails) #Color to the error rows
        createPoints(coordPoint) #function invocation to create observations on the map

    """Create the lines layer from the imported csv file"""
    def createLineLayer(self):
        layerLine = [] #List of data needed to create the lines of each observation
        row_indx_fail = 0
        row_fails = [] #List of rows with errors at the data needed to create the lines
        for feature in range(self.model.rowCount()):
                currentRow = self.model.takeRow(feature)
                self.model.insertRow(feature,currentRow)
                try:
                    x = float(currentRow[INDX_X].text())
                    y = float(currentRow[INDX_Y].text())
                    azimut = float(currentRow[INDX_AZMT].text())
                    puissance_signal = float(currentRow[INDX_SIGN].text())
                    niveau_filtre = float(currentRow[INDX_NIV_FILT].text())
                    distance = puissance_signal + niveau_filtre
                    res_distance = 1-(distance-ONE_KM)*PAS
                    #layerLine.append([x,y,azimut,puissance_signal,niveau_filtre])
                    layerLine.append([x,y,azimut,res_distance])
                except:
                    print('Fatal error creating LineLayer - Data error at line ',row_indx_fail+1)
                    row_fails.append(row_indx_fail)
                row_indx_fail += 1
        self.color(row_fails) #Color to the error rows
        createLines(layerLine) #function invocation to create lines on the map
 
    """Validation header function"""
    def header_validation(self,header_in):
        """Lists of error analysing 
            Comparison of the input header and the expected header"""
        
        #lists of errors found
        warning = [] 
        fatal = []

        try:
            if header_in[INDX_ID_OBS].text() != HEADERS[0]:
                fatal.append('id_observation error')
            if header_in[INDX_ID_INDV].text() != HEADERS[1]:
                fatal.append('id_individu fatal error')
            if header_in[INDX_NOM_INDV].text() != HEADERS[2]:
                fatal.append('nom_individu fatal error')
            if header_in[INDX_DATE].text() != HEADERS[3]:
                fatal.append('date fatal error')
            if header_in[INDX_X].text() != HEADERS[4]:
                fatal.append('coordonnees_wgs84_n fatal error')
            if header_in[INDX_Y].text() != HEADERS[5]:
                fatal.append('coordonnees_wgs84_e fatal error')
            if header_in[INDX_AZMT].text() != HEADERS[6]:
                fatal.append('azimut fatal error')
            if header_in[INDX_NIV_FILT].text() != HEADERS[7]:
                fatal.append('niveau_filtre fatal error')
            if header_in[INDX_SIGN].text() != HEADERS[8]:
                fatal.append('puissance_signal fatal error')
            if header_in[INDX_COMM].text() != HEADERS[9]:
                fatal.append('commentaire fatal error')
        except:
            fatal.append('Fatal error validating header')
        return warning,fatal
        
    """Initialization table and BatLayer"""
    def initializeBatLayer(self):
        filenames = self.getfile()
        if filenames:
            self.createTable(filenames)
            self.createBatLayer()
        else:
            print('Error importing file')

    """Import csv file function"""
    def getfile(self):        
        #Select and import csv file
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("Text files (*.csv)")        
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.currentProjectText.setText(filenames[0]) # Set the name project in the label text
            return filenames[0]
            
    """Create table from the project sended"""
    def createTable(self,filenames):
        #Configuration type of modeling and visualization of the data table
        self.model = QtGui.QStandardItemModel(self)
        qTable = self.tableView
        #New reference to HEADERS 
        headers = []
        for h in HEADERS:
            headers.append(h)
        flag_header = 0 #Check if the header is already in the model

        """Open the imported file csv
            Extract the rows from the file and save them in the Items list
            After the header validation, if there are not errors header and rows are added to the model
            """
        with open(filenames, "rb") as fileInput:
            for row in csv.reader(fileInput):  
                items = [
                    QtGui.QStandardItem(field.decode('utf-8'))
                    for field in row
                ]
                if flag_header == 0:
                    warning_header,fatal_header = self.header_validation(items)
                    if (len(fatal_header) == 0 and len(warning_header) == 0):
                        for it in range (10,len(items)):
                            headers.append(items[it].text())
                        self.model.setHorizontalHeaderLabels(headers)
                    flag_header += 1
                else:
                    if (len(fatal_header) == 0 and len(warning_header) == 0):
                        self.model.appendRow(items)
                
        if (len(fatal_header) == 0 and len(warning_header) == 0):
            qTable.setModel(self.model)
            qTable.resizeColumnsToContents()
            qTable.resizeRowsToContents()
        else:
            print('errors : ',fatal_header,warning_header)
            self.currentProjectText.clear()

    """Save current project"""
    def save(self):
        try:
            #Read and open the current project 
            fileName = self.currentProjectText.toPlainText()
            output_file = open(fileName, 'w')
            #Write into current file project the table content 
            with open(fileName, "wb") as fileOutput:
                writer = csv.writer(fileOutput)        
                line_aux = []
                for n in range(self.model.columnCount()):
                    line_aux.append((self.model.horizontalHeaderItem(n).text()).encode('utf-8').strip())
                line = ','.join(line_aux) + '\n'
                unicode_line = line
                output_file.write(unicode_line)
                for feature in range(self.model.rowCount()):
                    line_aux = []
                    currentRow = self.model.takeRow(feature)
                    self.model.insertRow(feature,currentRow)
                    for n in range(self.model.columnCount()):
                        line_aux.append((currentRow[n].text()).encode('utf-8').strip())
                    line = ','.join(line_aux) + '\n'
                    unicode_line = line
                    output_file.write(unicode_line)
                output_file.close()
            print('File already saved')
        except: 
            print('Error saving file')

    """Save the project with other name"""
    def save_as(self):
        try:
            #Allows user to select the destination and save after
            filename = QFileDialog.getSaveFileName(self, "Select output file ","", '*.csv')
            self.currentProjectText.setText(filename+'.csv')
            self.save()
        except:
            print('Error saving file')
