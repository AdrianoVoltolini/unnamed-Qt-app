
from PySide6 import QtWidgets, QtGui, QtCore
from app_stats import StatWindow
from app_input import InputWindow
from app_home import HomeWindow
import pandas as pd
import bz2

# __version__="0.0.1"

class RootWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,315,700)
        
        self.widget_main = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_top = QtWidgets.QHBoxLayout()
        self.scrollatore = QtWidgets.QScrollArea()

        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)
        self.layout_main.addLayout(self.layout_top)

        self.dataframe = pd.DataFrame()
        self.chosen_dataset = ""
        self.finestre = [HomeWindow(),InputWindow(),StatWindow()]

        for w in self.finestre:
            bottone =  QtWidgets.QPushButton(w.objectName())
            self.layout_top.addWidget(bottone)
            bottone.pressed.connect(self.cambiaFinestra)
            w.setParent(self)
            self.layout_main.addWidget(w)
            if w.objectName() != "HOME":
                w.hide()
        
        self.scrollatore.setWidgetResizable(True)
        self.scrollatore.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollatore.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollatore.setWidget(self.widget_main)
        self.setCentralWidget(self.scrollatore)

    def cambiaFinestra(self):
        for w in self.finestre:
            w.hide()

        for i in range(self.layout_top.count()):
            if self.layout_top.itemAt(i).widget().isDown():
                self.layout_top.itemAt(i).widget().setEnabled(False)
                self.finestre[i].load()
                self.finestre[i].show()
            else:
                self.layout_top.itemAt(i).widget().setEnabled(True)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        for w in self.children()[1:]:
            w.resize(self.size())
        return super().resizeEvent(event)
    
    def salvaDataframe(self):
        with bz2.open(f"datasets//{self.chosen_dataset}.bz2","wb") as output:
            output.write(self.dataframe.to_csv().encode())


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    rootWindow = RootWindow()
    rootWindow.show()
    app.exec()
