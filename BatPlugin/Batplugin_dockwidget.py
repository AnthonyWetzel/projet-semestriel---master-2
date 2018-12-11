# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BatPluginDockWidget
                             -------------------
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

from .createRemoveLayers import createLayerLines, createLayerPoints, clearLayer
from .algorithmNewPoint import dst

from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsExpression

from .compat import get_field
from .compat2qgis import QDockWidget, QTableView

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Batplugin_dockwidget_base.ui'))

class BatPluginDockWidget(QDockWidget, FORM_CLASS):

    """Global variables """
    #logCount = 0
    w = QWidget()
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

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(BatPluginDockWidget, self).__init__(parent)
        self.setupUi(self)
        """
            Plugin actions"""
        """Clear old layers"""
        clearLayer('lineLayer')
        clearLayer('batLayer')
        self.logText.clear()
        self.logText.insertPlainText('----------------------------------------\nFind here log messages\n----------------------------------------\n')
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
        
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    """Refresh current project after modifications"""
    def refresh(self):
        try:            
            self.save()
            fileName = self.currentProjectText.toPlainText()
            self.createTable(fileName)
            self.createBatLayer()
            clearLayer('lineLayer')
            self.logText.insertPlainText('Project refresh \n')
        except:
            QMessageBox.critical(self.w, "Message", "Refreshing view error.")

    """Color the rows that have errors"""
    def color(self,row_indx_fail):
        for col in range(self.model.columnCount()):
            for i in range(len(row_indx_fail)):

               self.model.setData(self.model.index(row_indx_fail[i]-1, col), QBrush(QColor(Qt.red).lighter()), QtCore.Qt.BackgroundRole)

    """Create the observations layer from the imported csv file"""
    def createBatLayer(self):
        coordPoint = [] # List of coordinates X,Y to add to the map
        row_indx_fail = 1
        row_fails = [] #List of rows with errors at the coordinates X and Y
        for feature in range(self.model.rowCount()):
                currentRow = self.model.takeRow(feature)
                self.model.insertRow(feature,currentRow)
                try:
                    coord_x = float(currentRow[self.INDX_X].text())
                    coord_y = float(currentRow[self.INDX_Y].text())
                    coordPoint.append([coord_y,coord_x])
                except:
                    self.logText.insertPlainText('Fatal error creating BatLayer - Coordinates fatal error at line  %d \n' % row_indx_fail)
                    #print('Fatal error creating BatLayer - Coordinates fatal error at line ',row_indx_fail+1)
                    row_fails.append(row_indx_fail)
                row_indx_fail += 1
        if len(row_fails) > 0:
            QMessageBox.information(self.w, "Message", "Error creating observations. Check the log.")
            self.color(row_fails) #Color to the error rows
        createLayerPoints(coordPoint) #function invocation to create observations on the map

    """Create the lines layer from the imported csv file"""
    def createLineLayer(self):
        try:
            layerLine = [] #List of data needed to create the lines of each observation
            row_indx_fail = 1
            row_fails = [] #List of rows with errors of the data needed to create the lines
            for feature in range(self.model.rowCount()):
                    currentRow = self.model.takeRow(feature)
                    self.model.insertRow(feature,currentRow)
                    try:
                        x = float(currentRow[self.INDX_X].text())
                        y = float(currentRow[self.INDX_Y].text())
                        azimut = float(currentRow[self.INDX_AZMT].text())
                        puissance_signal = float(currentRow[self.INDX_SIGN].text())
                        niveau_filtre = float(currentRow[self.INDX_NIV_FILT].text())
                        distance = puissance_signal + niveau_filtre
                        res_distance = 1-(distance-self.ONE_KM)*self.PAS
                        #layerLine.append([x,y,azimut,puissance_signal,niveau_filtre])
                        layerLine.append([x,y,azimut,res_distance])
                    except:
                        self.logText.insertPlainText('Fatal error creating LineLayer - Data error at line %d \n' % row_indx_fail)
                        #print('Fatal error creating LineLayer - Data error at line ',row_indx_fail+1)
                        row_fails.append(row_indx_fail)
                    row_indx_fail += 1
            if len(row_fails) > 0:
                QMessageBox.critical(self.w, "Message", "Error creating lines. Check the log.")
                self.color(row_fails) #Color to the error rows
            if len(layerLine) > 0:
                createLayerLines(layerLine) #function invocation to create lines on the map
        except:
            self.logText.insertPlainText('Fatal error creating LineLayer \n')
            QMessageBox.critical(self.w, "Message", "Fatal error creating lines.")

    """Validation header function"""
    def header_validation(self,header_in):
        """Lists of error analysing 
            Comparison of the input header and the expected header"""
        
        #lists of errors found
        warning = [] 
        fatal = []

        try:
            if header_in[self.INDX_ID_OBS].text() != self.HEADERS[self.INDX_ID_OBS]:
                fatal.append('id_observation error')
            if header_in[self.INDX_ID_INDV].text() != self.HEADERS[self.INDX_ID_INDV]:
                fatal.append('id_individu fatal error')
            if header_in[self.INDX_NOM_INDV].text() != self.HEADERS[self.INDX_NOM_INDV]:
                fatal.append('nom_individu fatal error')
            if header_in[self.INDX_DATE].text() != self.HEADERS[self.INDX_DATE]:
                fatal.append('date fatal error')
            if header_in[self.INDX_X].text() != self.HEADERS[self.INDX_X]:
                fatal.append('coordonnees_wgs84_n fatal error')
            if header_in[self.INDX_Y].text() != self.HEADERS[self.INDX_Y]:
                fatal.append('coordonnees_wgs84_e fatal error')
            if header_in[self.INDX_AZMT].text() != self.HEADERS[self.INDX_AZMT]:
                fatal.append('azimut fatal error')
            if header_in[self.INDX_NIV_FILT].text() != self.HEADERS[self.INDX_NIV_FILT]:
                fatal.append('niveau_filtre fatal error')
            if header_in[self.INDX_SIGN].text() != self.HEADERS[self.INDX_SIGN]:
                fatal.append('puissance_signal fatal error')
            if header_in[self.INDX_COMM].text() != self.HEADERS[self.INDX_COMM]:
                fatal.append('commentaire fatal error')
        except:
            fatal.append('Fatal error validating header')
            self.logText.insertPlainText('Fatal error validating header.\n')
        return warning,fatal
        
    """Initialization table and BatLayer"""
    def initializeBatLayer(self):
        filenames = self.getfile()
        if filenames:
            self.createTable(filenames)
            self.createBatLayer()
        else:
            self.logText.insertPlainText('Error initializing BatLayer.\n')
            QMessageBox.information(self.w, "Message", "No project imported.")            

    """Import csv file function"""
    def getfile(self):        
        try:
            #Select and import csv file
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.AnyFile)

            dlg.setNameFilter("Text files (*.csv)")

            if dlg.exec_():
                filenames = dlg.selectedFiles()
                self.currentProjectText.setText(filenames[0]) # Set the name project in the label text
                self.logText.insertPlainText('Project successfully imported .\n')
                return filenames[0]
        except:
            self.logText.insertPlainText('Error importing file .\n')
            QMessageBox.critical(self.w, "Message", "Error importing file.")

    """Create table from the project sended"""
    def createTable(self,filenames):
        #Configuration type of modeling and visualization of the data table
        self.model = QtGui.QStandardItemModel(self)
        qTable = self.tableView

        #New reference to HEADERS 
        headers = []
        for h in self.HEADERS:
            headers.append(h)
        flag_header = 0 #Check if the header is already in the model

        """Open the imported file csv
            Extract the rows from the file and save them in the Items list
            After the header validation, if there are not errors header and rows are added to the model
            """
        with open(filenames, "rt") as fileInput:
            for row in csv.reader(fileInput):  
                items = [
                    QtGui.QStandardItem(get_field(field))
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
            self.logText.insertPlainText('Table successfully created.\n')
        else:
            QMessageBox.critical(self.w, "Message", "Header structure error. Check the log.")
            self.logText.insertPlainText('Imposible to create table. Table structure incorrect.\n')
            for err in fatal_header:
                self.logText.insertPlainText(err)
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
            self.logText.insertPlainText('Project successfully saved .\n')
        except: 
            self.logText.insertPlainText('Imposible to save.\n')
            QMessageBox.critical(self.w, "Message", 'Error saving project')

    """Save the project with other name"""
    def save_as(self):
        try:
            #Allows user to select the destination and save after
            filename = QFileDialog.getSaveFileName(self, "Select output file ","", '*.csv')
            if (filename!=''):
                self.currentProjectText.setText(filename+'.csv')
                self.save()
        except:
            QMessageBox.critical(self.w, "Message", 'Error saving project. Check the log')

"""
    def setTableWidth(self):
        
        width = self.model.verticalHeader().width()
        print('first',width)
        width += self.model.horizontalHeader().length()
        print('second',width)
        if self.model.verticalScrollBar().isVisible():
            width += self.model.verticalScrollBar().width()
        width += self.model.frameWidth() * 2
        print('third',width)
        self.model.setFixedWidth(width)

    def resizeEvent(self, event):
        self.setTableWidth()
        super(BatPluginDockWidget, self).resizeEvent(event)"""