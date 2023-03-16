import os
import sys

# Adiciona o diretório "Pacotes" ao sys.path
pacotes_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.insert(0, pacotes_dir)

from Views import Interface as itf
from itfLogica import logicaInterface

class InfoCalcsManager:
    def __init__(self, familiasList):

        self.valorPorDia = int()
        self.valorTotalGasto = int()
        self.totalDias = int()

        self.familiaList = familiasList

        self.valuesFerias = {
            "totalDias" : self.totalDias,
            "valorTotalGasto" : self.valorTotalGasto,
            "valorPorDia" : self.valorPorDia
        }

    def restartCalcValues(self):
        self.valorPorDia = float()
        self.valorTotalGasto = float()
        self.totalDias = int()

        for fam in self.familiaList:
            for part in fam.partsList:
                self.totalDias += int(part.dias)
                self.valorTotalGasto += float(part.pagou)

        self.valuesFerias["totalDias"] = self.totalDias
        self.valuesFerias["valorTotalGasto"] = self.valorTotalGasto
        self.valuesFerias["valorPorDia"] = self.valorTotalGasto / self.totalDias

    def attValuesViagem(self, dias=int(), val=float(), sum=True, modo="unico", elementsList=list()):

        if modo == "unico":
            if sum:
                self.totalDias += int(dias)
                self.valorTotalGasto += float(val)
            else:
                self.totalDias -= int(dias)
                self.valorTotalGasto -= float(val)

            if self.valorTotalGasto != 0 and self.totalDias != 0:
                self.valorPorDia = self.valorTotalGasto / self.totalDias
            else:
                self.valorPorDia = 0
       
        elif modo == "lista":
            removedDias, removedValor = int(), float()

            for element in elementsList:
                removedDias += int(element.dias)
                removedValor += float(element.pagou)

                self.totalDias -= removedDias
                self.valorTotalGasto -= removedValor

            if self.valorTotalGasto != 0 and self.totalDias != 0:
                self.valorPorDia = self.valorTotalGasto / self.totalDias
            else:
                self.valorPorDia = 0

            return removedDias, removedValor


familiasList = []
windowBase = itf.layoutBase(familiasList)
estado = 'base' 

feriasCalc = logicaInterface(windowBase, familiasList, estado, InfoCalcsManager)

while True:
    feriasCalc.mainLoop()
