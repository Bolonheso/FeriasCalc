class Participante:
    def __init__(self, id, nome, dias, pagou):
        self.id = id
        self.deve = float()

        self.nome = nome
        self.dias = dias
        self.pagou = pagou

    def copy(self):
        return Participante(self.id, self.nome, self.dias, self.pagou)


class Familia:
    def __init__(self, id, pagante, partsList):
        self.gastoTotal = float()
        self.id = id
        self.pagante = pagante
        self.partsList = partsList

    def copy(self):
        return Familia(self.id, self.pagante, self.partsList)

valTotal = float()
familiasList = list()
diasViagem = list()
totalDiasPagos = int()
