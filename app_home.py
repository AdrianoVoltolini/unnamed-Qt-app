
from PySide6 import QtWidgets
from io import BytesIO
import pandas as pd
import bz2

class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        #finestra principale
        super().__init__()
        self.setObjectName("HOME")
        self.load()

    def load(self):
        pass