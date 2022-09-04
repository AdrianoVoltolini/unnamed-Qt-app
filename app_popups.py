
from PySide6 import QtWidgets
import pandas as pd
from os import listdir

class PopupVarCreator(QtWidgets.QDialog):
    #classe per il popup del pulsante che crea una nuova variabile
    def __init__(self,finestra):
        super().__init__()

        self.finestra = finestra
        self.output_nome = ""

        self.scegli_nome = QtWidgets.QLineEdit("choose a name")
        self.scegli_nome.textChanged.connect(self.controllaNome)

        self.scegli_tipo = QtWidgets.QComboBox()
        self.scegli_tipo.addItems(["Regression","Classification","String","Default"])
        self.scegli_tipo.currentIndexChanged.connect(self.attivaTesto)

        self.bottone_finito = QtWidgets.QPushButton("create") 
        self.bottone_finito.setEnabled(False)       
        self.bottone_finito.pressed.connect(self.finitore)

        self.input_parametro = QtWidgets.QTextEdit("one class or parameter per line")
        self.input_parametro.setEnabled(False)
        self.input_parametro.textChanged.connect(self.controllaParametri)

        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.scegli_nome)
        self.layout_main.addWidget(self.scegli_tipo)
        self.layout_main.addWidget(self.input_parametro)
        self.layout_main.addWidget(self.bottone_finito)

        self.setLayout(self.layout_main)

    def finitore(self):
        # funzione per creare nome e aggiungere colonna a dataframe
        lista_nomi = [self.scegli_tipo.currentText()[0],self.scegli_nome.text()]
        if self.scegli_tipo.currentText()[0] == "C":
            lista_nomi = lista_nomi + self.input_parametro.toPlainText().split("\n")
        elif self.scegli_tipo.currentText()[0] == "D":
            if self.scegli_nome.text() == "steam":
                lista_nomi = lista_nomi + self.input_parametro.toPlainText().split("\n")

        self.output_nome = "_".join(lista_nomi)

        self.finestra.root.dataframe = pd.concat(
            [self.finestra.root.dataframe,pd.Series(name=self.output_nome,dtype="object")],axis=1)
        self.finestra.load()
        self.close()

    def attivaTesto(self):
        #attiva o disattiva quadretto di testo dove mettere parametri
        if self.scegli_tipo.currentText()[0] =="C":
            self.input_parametro.setEnabled(True)
        elif self.scegli_tipo.currentText()[0] == "D":
            if self.scegli_nome.text() == "steam":
                self.input_parametro.setEnabled(True)
        else:
            self.input_parametro.setEnabled(False)
    
    def controllaParametri(self):
        #controlla che non ci sia il carattere _ nei parametri
        if "_" in self.input_parametro.toPlainText():
            self.bottone_finito.setEnabled(False)
        else:
            self.bottone_finito.setEnabled(True)
    
    def controllaNome(self):
        #controlla che non ci sia già una variabile con lo stesso nome
        if self.scegli_nome.text() in [x.split("_")[1] for x in self.finestra.root.dataframe.columns]:
            self.bottone_finito.setEnabled(False)
            self.bottone_finito.setText("choose a new name")
        else:
            self.bottone_finito.setEnabled(True)
            self.bottone_finito.setText("create")




class PopupEditor(QtWidgets.QDialog):
    #classe per il popup del pulsante che edita una nuova variabile
    def __init__(self,finestra,indice):
        super().__init__()

        self.finestra = finestra
        self.indice = indice
        self.nome = self.finestra.bottoni_edit[self.indice].objectName()

        self.layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout_main)

        self.nome_editore = QtWidgets.QLineEdit(self.nome)
        self.layout_main.addWidget(self.nome_editore)
        self.nome_editore.textChanged.connect(self.controllaNome)

        self.layout_bottoni = QtWidgets.QHBoxLayout()
        self.layout_main.addLayout(self.layout_bottoni)

        self.bottone_eliminatore = QtWidgets.QPushButton("DELETE IT")
        self.layout_bottoni.addWidget(self.bottone_eliminatore)
        self.bottone_eliminatore.pressed.connect(self.eliminatore)

        self.bottone_salvatore = QtWidgets.QPushButton("SAVE")
        self.layout_bottoni.addWidget(self.bottone_salvatore)
        self.bottone_salvatore.pressed.connect(self.salvatore)
        self.bottone_salvatore.setEnabled(False)


    def eliminatore(self):
        #elimina variabile dal dataframe
        self.finestra.root.dataframe = self.finestra.root.dataframe.drop(
            self.finestra.root.dataframe.columns[self.indice],axis=1)
        self.finestra.load()
        self.close()


    def salvatore(self):
        # salva cambiamenti fatti
        self.finestra.root.dataframe = self.finestra.root.dataframe.rename(
            {self.nome : self.nome_editore.text()},axis=1)
        self.finestra.load()
        self.close()
    
    def controllaNome(self):
        #controlla che non ci sia già una variabile con lo stesso nome
        if self.nome_editore.text().split("_")[1] in [x.split("_")[1] for x in self.finestra.root.dataframe.columns]:
            self.bottone_salvatore.setEnabled(False)
        else:
            self.bottone_salvatore.setEnabled(True)
            self.bottone_salvatore.setText("SAVE")

class PopupDatasetCreator(QtWidgets.QDialog):
    def __init__(self,root):
        super().__init__()
        self.root = root

        self.layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout_main)

        self.nome_editore = QtWidgets.QLineEdit("untitled")
        self.layout_main.addWidget(self.nome_editore)
        self.nome_editore.textChanged.connect(self.controllaNome)

        self.bottone_salvatore = QtWidgets.QPushButton("SAVE")
        self.layout_main.addWidget(self.bottone_salvatore)
        self.bottone_salvatore.pressed.connect(self.salvatore)
        self.bottone_salvatore.setEnabled(False)


    def controllaNome(self):
        if ".".join([self.nome_editore.text(),"bz2"]) in listdir("./datasets"):
            self.bottone_salvatore.setText("choose a new name")
            self.bottone_salvatore.setEnabled(False)
        else:
            self.bottone_salvatore.setText("SAVE")
            self.bottone_salvatore.setEnabled(True)
    
    def salvatore(self):
        self.root.chosen_dataset = self.nome_editore.text()
        self.root.salvaDataframe()
        self.close()




