import pickle
from . import dados

class dataManager:
    def __init__(self, event,value,win):
        self.event = event
        self.value = value
        self.win = win

    def delElements(self, elementsList, window, prefix=''):
        removedElements = []

        for element in elementsList[:]:
            if self.win == window and self.value[f'{prefix}{element.id}' if prefix else element.id]:
                removedElements.append(element.copy())
                elementsList.remove(element)
        return removedElements

    def createPart(self, nome, valorGasto, dias, id, partsList):
        part = dados.Participante(
            id=id,
            nome=nome.strip().capitalize(),
            dias=dias,
            pagou=valorGasto
        )

        partsList.append(part)

    def verificarInfoPart(self, valorFloat, diasInt):
        chave1, chave2 = False, False

        diasInt = diasInt.strip()
        valorFloat = valorFloat.strip().replace("," , "")
        valorFloat = valorFloat.replace("." , "")

        if diasInt and diasInt.isdigit():
   
            chave2 = True

        if valorFloat and valorFloat.isdigit():
            chave1 = True

        if chave1 and chave2:
            return True
        else:
            return False
    

    def createFamily(self, id, pagante, partsList, familiasList):

        fam = dados.Familia(
            id=id,
            pagante=pagante,
            partsList=partsList
        )

        familiasList.append(fam)

    def attValuesFamilys(self, familys, valorPorDia):

        for fam in familys:
            valorTotalFamily = float()
            for part in fam.partsList:
                part.deve = float(part.dias) * valorPorDia
                valorTotalFamily += part.deve
            fam.gastoTotal = valorTotalFamily


        