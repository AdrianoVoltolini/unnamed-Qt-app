
import pandas as pd
from PySide6 import QtWidgets, QtGui
from datetime import datetime
from app_popups import PopupVarCreator, PopupEditor



class InputWindow(QtWidgets.QMainWindow):
    def __init__(self):
        #finestra principale
        super().__init__()
        self.setObjectName("INPUT")

    
    def load(self):
        #ricarica finestra principale
        self.root = self.parent().parent().parent().parent()
        self.widget_main = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)

        if self.root.dataframe.shape == (0,0):
            self.layout_main.addWidget(QtWidgets.QLabel("( ͡° ͜ʖ ͡°) hi"))

        self.bottoni_edit = []
        self.widget_inputs = []

        for index in range(len(self.root.dataframe.columns)):
            cornice = self.creaCornice(index)
            self.layout_main.addWidget(cornice)
            
        self.bottone_salvatore = QtWidgets.QPushButton("SAVE DATA")
        self.layout_main.addWidget(self.bottone_salvatore)
        self.bottone_salvatore.pressed.connect(self.salvatore)

        self.bottone_showatore = QtWidgets.QPushButton("SHOW DATA")
        self.layout_main.addWidget(self.bottone_showatore)
        self.bottone_showatore.pressed.connect(self.showatore)

        self.bottone_creatore = QtWidgets.QPushButton("ADD NEW VARIABLE")
        self.layout_main.addWidget(self.bottone_creatore)
        self.bottone_creatore.pressed.connect(self.creatore)

        
    def editore(self):
        #elimina variabile dalla pagina principale e dal dataframe
        for indice in range(len(self.bottoni_edit)):
            if self.bottoni_edit[indice].isDown():
                PopupEditor(self,indice).exec()
                break

    def creatore(self):
        #apre popup per creare nuova variabile
        creatore = PopupVarCreator(self)
        creatore.exec()
    
    def creaCornice(self,indice):
            #funzione che crea gli elementi che mostrano le variabili
            #nella pagina principale
            colonna = self.root.dataframe.columns[indice]
            layout_sub = QtWidgets.QHBoxLayout()
            layout_sub.setObjectName(f"layout_sub_{indice}")
            cornice =  QtWidgets.QGroupBox()
            cornice.setObjectName(f"cornice_{indice}")
            cornice.setLayout(layout_sub)
            if colonna[0] == "D":

                if colonna == "D_time":
                    layout_sub.addWidget(QtWidgets.QLabel(colonna[2:]))
                    input_object = QtWidgets.QLabel(
                        datetime.now().isoformat(sep=" ",timespec="minutes"))

                elif colonna[0:7] == "D_steam":
                    layout_sub.addWidget(QtWidgets.QLabel(colonna[2:7]))
                    from steam.webapi import WebAPI
                    try:
                        api = WebAPI(key="71C0364A066799AFA860E6626EB64748")
                        giochi = api.IPlayerService.GetRecentlyPlayedGames(
                            steamid=colonna[8:],count=14)["response"]["games"]
                        input_object = QtWidgets.QLabel(str(sum(x["playtime_2weeks"] for x in giochi)))
                    except:
                        input_object = QtWidgets.QLabel()

            elif colonna[0] == "R":
                layout_sub.addWidget(QtWidgets.QLabel(colonna[2:]))
                input_object = QtWidgets.QLineEdit()
                input_object.setValidator(QtGui.QDoubleValidator())
                layout_sub.addWidget(input_object)
                input_object.setFrame(0)

            elif colonna[0] == "C":
                lista_temp = colonna.split("_")
                lunghezza = len(lista_temp[0]) + len(lista_temp[1]) +1
                lista_var = lista_temp[2:]
                layout_sub.addWidget(QtWidgets.QLabel(colonna[2:lunghezza]))
                input_object = QtWidgets.QComboBox()
                input_object.addItems(lista_var)

            else:
                layout_sub.addWidget(QtWidgets.QLabel(colonna[2:]))
                input_object = QtWidgets.QPlainTextEdit()
                input_object.setFrameStyle(0)

            layout_sub.addWidget(input_object)
            bottone_edit = QtWidgets.QPushButton("EDIT")
            self.bottoni_edit.append(bottone_edit)
            self.widget_inputs.append(input_object)
            bottone_edit.setFixedWidth(50)
            bottone_edit.setObjectName(colonna)
            bottone_edit.pressed.connect(self.editore)
            layout_sub.addWidget(bottone_edit)

            return cornice

    def showatore(self):
        print(self.root.dataframe)

    def salvatore(self):
        self.newline = []
        if self.root.chosen_dataset != "":
            for i in self.widget_inputs:
                try:
                    self.newline.append(i.text())
                except:
                    try:
                        self.newline.append(i.currentText())
                    except:
                        self.newline.append(i.toPlainText())

            self.root.dataframe.loc[self.root.dataframe.shape[0],:] = pd.Series(self.newline,index=self.root.dataframe.columns)
            self.root.salvaDataframe()
            self.load()

