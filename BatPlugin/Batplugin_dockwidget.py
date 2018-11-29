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

import os

from createLineLayer import *
from algorithmNewPoint import *

from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsExpression
try:
    from qgis.PyQt.QtGui import QDockWidget
except:
    from qgis.PyQt.QtWidgets import QDockWidget

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
	
	self.calculNewPoint.clicked.connect(self.slotCalculNewPoint)


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

    def slotCalculNewPoint(self):
        layer=self.ifaceRef.activeLayer()
	createLine(layer.getFeatures(),'coordonnees_wgs84_n','coordonnees_wgs84_e')

