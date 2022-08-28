
from PySide6 import QtWidgets

class StatWindow(QtWidgets.QMainWindow):
    def __init__(self,padre):
        super().__init__()
        self.padre = padre
        self.setGeometry(self.padre.geometry())
        self.load()

    def load(self):
        self.widget_main = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.scrollatore = QtWidgets.QScrollArea()

        self.layout_top = QtWidgets.QHBoxLayout()
        
        self.bottone_home = QtWidgets.QPushButton("HOME")
        self.layout_top.addWidget(self.bottone_home)
        self.bottone_home.pressed.connect(self.cambiaFinestra)
        self.bottone_stat = QtWidgets.QPushButton("STAT")
        self.bottone_stat.setEnabled(False)

        self.layout_top.addWidget(self.bottone_stat)
        self.layout_main.addLayout(self.layout_top)

        self.scrollatore.setWidgetResizable(True)
        self.scrollatore.setWidget(self.widget_main)

        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.scrollatore)

    def cambiaFinestra(self):
        self.padre.setGeometry(self.geometry())
        self.padre.show()
        self.hide()
        

