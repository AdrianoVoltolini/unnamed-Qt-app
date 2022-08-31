
from PySide6 import QtWidgets
from io import BytesIO
import pandas as pd
import bz2
from os import listdir

class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        #finestra principale
        super().__init__()
        self.setObjectName("HOME")
        self.load()

    def load(self):

        self.widget_main = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)

        self.box_datasets = QtWidgets.QGroupBox()
        self.layout_datasets = QtWidgets.QVBoxLayout()
        self.box_datasets.setTitle("Existing Datasets:")
        self.box_datasets.setLayout(self.layout_datasets)
        self.layout_main.addWidget(self.box_datasets)

        self.bottoni = []

        for d in listdir("./datasets"):
            bottone = QtWidgets.QPushButton(d[:-4])
            bottone.pressed.connect(self.datasetPremuto)
            self.bottoni.append(bottone)
            self.layout_datasets.addWidget(bottone)

        self.bottone_crea = QtWidgets.QPushButton("CREATE NEW DATASET")
        self.layout_main.addWidget(self.bottone_crea)

    def datasetPremuto(self):
        self.root = self.parent().parent().parent().parent()
        for b in self.bottoni:
            if b.isDown():
                with bz2.open(f"datasets//{b.text()}.bz2","rb") as input:
                    dataset_binary = input.read()
                self.root.dataframe = pd.read_csv(BytesIO(dataset_binary),index_col=0)
                self.root.chosen_dataset = b.text()
                b.setEnabled(False)