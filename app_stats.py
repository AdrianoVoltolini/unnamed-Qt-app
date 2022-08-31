
from PySide6 import QtWidgets
from io import BytesIO
import pandas as pd
import bz2


class StatWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("STATS")


    def load(self):
        self.root = self.parent().parent().parent().parent()
        self.widget_main = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)


        self.response = QtWidgets.QComboBox()
        self.variables = [x.split("_")[1] for x in self.root.dataframe.columns]
        self.response.addItems(self.variables)
        self.layout_response = QtWidgets.QHBoxLayout()
        self.layout_response.addWidget(QtWidgets.QLabel("Response:"))
        self.layout_response.addWidget(self.response)
        self.layout_main.addLayout(self.layout_response)
        self.layout_checkboxes = QtWidgets.QHBoxLayout()
        self.layout_checksL = QtWidgets.QVBoxLayout()
        self.layout_checksR = QtWidgets.QVBoxLayout()
        self.layout_checkboxes.addLayout(self.layout_checksL)
        self.layout_checkboxes.addLayout(self.layout_checksR)

        self.cornice_checkboxes = QtWidgets.QGroupBox()
        self.cornice_checkboxes.setTitle("Predictors:")
        self.cornice_checkboxes.setLayout(self.layout_checkboxes)
        self.layout_main.addWidget(self.cornice_checkboxes)

        self.checkgroup = QtWidgets.QButtonGroup()
        self.checkgroup.setExclusive(False)


        for x in range(len(self.variables)):
            bottone = QtWidgets.QCheckBox(self.variables[x])
            self.checkgroup.addButton(bottone)
            if x%2 ==  0:
                self.layout_checksL.addWidget(bottone)
            else:
                self.layout_checksR.addWidget(bottone)

    def cambiaFinestra(self):
        self.parent().findChild(QtWidgets.QMainWindow,name="input").show()
        self.hide()
        

