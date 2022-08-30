
import bz2
from PySide6 import QtWidgets
import pandas as pd

class PopupCreator(QtWidgets.QDialog):
    #classe per il popup del pulsante che crea una nuova variabile
    def __init__(self,finestra):
        super().__init__()

        self.finestra = finestra
        self.output_nome = ""

        self.scegli_nome = QtWidgets.QLineEdit("choose a name")

        self.scegli_tipo = QtWidgets.QComboBox()
        self.scegli_tipo.addItems(["Regression","Classification","String","Default"])
        self.scegli_tipo.currentIndexChanged.connect(self.attivaTesto)

        self.bottone_finito = QtWidgets.QPushButton("create")        
        self.bottone_finito.pressed.connect(self.finitore)

        self.input_parametro = QtWidgets.QTextEdit("one class or parameter per line")
        self.input_parametro.setEnabled(False)
        self.input_parametro.textChanged.connect(self.controllatore)

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
        self.finestra.dataframe = pd.concat([self.finestra.dataframe,pd.Series(name=self.output_nome,dtype="object")],axis=1)
        with bz2.open("compressed.bz2","wb") as output:
            output.write(self.finestra.dataframe.to_csv().encode())
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
    
    def controllatore(self):
        #controlla che non ci sia il carattere _ nei parametri
        if "_" in self.input_parametro.toPlainText():
            self.bottone_finito.setEnabled(False)
        else:
            self.bottone_finito.setEnabled(True)



class PopupEditor(QtWidgets.QDialog):
    #classe per il popup del pulsante che edita una nuova variabile
    def __init__(self,finestra,indice):
        super().__init__()

        self.finestra = finestra
        self.indice = indice
        self.nome = self.finestra.bottoni_edit[self.indice].objectName()

        self.nome_editore = QtWidgets.QLineEdit(self.nome)
        self.bottone_eliminatore = QtWidgets.QPushButton("DELETE IT")
        self.bottone_eliminatore.pressed.connect(self.eliminatore)

        self.bottone_salvatore = QtWidgets.QPushButton("SAVE")
        self.bottone_salvatore.pressed.connect(self.salvatore)

        self.layout_bottoni = QtWidgets.QHBoxLayout()
        self.layout_bottoni.addWidget(self.bottone_salvatore)
        self.layout_bottoni.addWidget(self.bottone_eliminatore)

        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.nome_editore)
        self.layout_main.addLayout(self.layout_bottoni)

        self.setLayout(self.layout_main)

    def eliminatore(self):
        #elimina variabile dal dataframe
        self.finestra.dataframe = self.finestra.dataframe.drop(self.finestra.dataframe.columns[self.indice],axis=1)
        self.bottone_eliminatore.setText("DELETED")
        self.bottone_eliminatore.setEnabled(False)
        self.nome_editore.setEnabled(False)


    def salvatore(self):
        # salva cambiamenti fatti
        self.finestra.dataframe = self.finestra.dataframe.rename({self.nome : self.nome_editore.text()},axis=1)
        with bz2.open("compressed.bz2","wb") as output:
            output.write(self.finestra.dataframe.to_csv().encode())
        self.finestra.load()
        self.close()
