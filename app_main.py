
from PySide6 import QtWidgets, QtGui
from app_stats import StatWindow
from app_input import InputWindow

# __version__="0.0.1"

class RootWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,270,600)
        
        self.windows = [StatWindow(),InputWindow()]
        for w in self.windows:
            w.setParent(self)
    
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        for w in self.windows:
            w.setFixedSize(self.size())
        return super().resizeEvent(event)


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    rootWindow = RootWindow()
    rootWindow.show()
    app.exec()
