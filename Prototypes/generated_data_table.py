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