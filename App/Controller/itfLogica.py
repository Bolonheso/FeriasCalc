import PySimpleGUI as sg
from Views import Interface as itf
from Models import dataManager as dm
from sys import exit

class logicaInterface: 
    def __init__(self, winBase, famsList, estado, InfoCalcsManager):
     
        self.windowBase = winBase
        self.familiasList = famsList
        
        self.parts = list()
        self.estado = estado
        self.estadoBefore = estado

        self.restartWinBase = False

        self.InfoCalcsManager = InfoCalcsManager(self.familiasList)
    
    def winLogin():
        pass

    def winBase(self):
        #if self.win == self.windowBase and self.event == sg.WIN_CLOSED:
        #    print(self.event)
        #    exit()   

        if self.win == self.windowBase and self.event == 'add' and self.estado == 'base':
            self.windowAddFam  = itf.layoutAddFamily(self.parts)
            self.estado = 'addFam'

        for fam in self.familiasList:
            if self.win == self.windowBase and self.event == fam.id:
                self.famToEdit = fam
                self.windowEditFamily = itf.layoutEditFamily(self.famToEdit)
                self.estado = 'editFam'
        
        if self.win == self.windowBase and self.event == 'delFam':
            removedFams = self.dataManager.delElements(self.familiasList, self.windowBase, 'Fd')
            
            for fam in removedFams: self.InfoCalcsManager.attValuesViagem(modo="lista", elementsList=fam.partsList)

            self.windowBase.close()
            self.windowBase = itf.layoutBase(self.familiasList)


            self.dataManager.attValuesFamilys(self.familiasList, self.InfoCalcsManager.valorPorDia) 

    def addFams(self):
        diasAdd, valAdd = int(), float()

        if self.win == self.windowAddFam and self.event == sg.WIN_CLOSED:
            self.windowAddFam.close()
            self.estado = 'base'
            self.parts.clear()

        if self.win == self.windowAddFam and self.event == 'cancelAddFam':
            self.windowAddFam.close()
            self.estado = 'base'
            self.parts.clear()

        if self.win == self.windowAddFam and self.event == 'addPart':
            
            if self.dataManager.verificarInfoPart(self.value['partValor'], self.value['partDias']):

                self.dataManager.createPart(
                    self.value['partNome'].capitalize(),
                    self.value['partValor'],
                    self.value['partDias'],
                    len(self.parts),

                    self.parts
                )
                
                partCreated = self.parts[-1]

                self.windowAddFam.find_element('defPagAddWin').update(values=[participante.nome for participante in self.parts])
                self.windowAddFam.extend_layout(self.windowAddFam['partsList'], [[sg.Text(f"{partCreated.id + 1}:"), sg.Text(f'{partCreated.nome}, R${partCreated.pagou} Dias: {partCreated.dias}'), sg.Checkbox('', key=f'P{len(self.parts)-1}')]])
            
            else:
                sg.popup("Por favor insira um número válido!", title="Erro", modal=True)

        if self.win == self.windowAddFam and self.event == 'delPart':
            
            self.dataManager.delElements(self.parts, self.windowAddFam, 'P')

            self.windowAddFam.close()
            self.windowAddFam = itf.layoutAddFamily(self.parts)

        #Verifica se existe pelo menos um participante, se sim, exibe o botão de remover participantes.
        if self.estado == 'addFam' and len(self.parts) >= 1:
            self.windowAddFam.find_element('delPart').update(visible=True)
        else:
            self.windowAddFam.find_element('delPart').update(visible=False)

        
        if self.win == self.windowAddFam and self.event == 'addFamily':
            
            if self.parts:
                
                self.dataManager.createFamily(
                    len(self.familiasList),
                    self.value['defPagAddWin'] if self.value['defPagAddWin'] != '' else self.parts[:][0].nome,
                    self.parts[:],
                    self.familiasList
                )

                #Atualiza os valores do total de dias e o valor gasto total da viagem, acrescentando o valor dos participantes
            
                for part in self.parts:
                    valAdd, diasAdd = float(), int()

                    valAdd += float(part.pagou)
                    diasAdd += int(part.dias)

                    self.InfoCalcsManager.attValuesViagem(diasAdd, valAdd)
                self.dataManager.attValuesFamilys(self.familiasList ,self.InfoCalcsManager.valorPorDia)

                famCriated = self.familiasList[-1]

                print(self.InfoCalcsManager.valorPorDia)
                self.dataManager.attValuesFamilys(self.familiasList, self.InfoCalcsManager.valorPorDia)

                if len(self.familiasList) == 1:
                    self.windowBase.close()
                    self.windowBase = itf.layoutBase(self.familiasList, ext=False)

                self.windowBase.extend_layout(self.windowBase['frameFamilias'], [[sg.Text(f'{famCriated.pagante} R$: {famCriated.gastoTotal:.2f}'), sg.Button('Editar', key=famCriated.id), sg.Checkbox('', key=f'Fd{famCriated.id}')]])
                self.estado = 'base' 
                self.windowAddFam.close()

                self.parts.clear()
            
            else:
                sg.popup("A familia deve ter pelo menos um participante!", "Erro", modal=True)

    def editFam(self):

        if self.win == self.windowEditFamily and self.event == 'confEditFam':
            if self.restartWinBase:
                self.windowBase.close()
                self.windowBase = itf.layoutBase(self.familiasList)
            
            self.windowEditFamily.close()
            self.estado = 'base'

        if self.win == self.windowEditFamily and self.event == sg.WIN_CLOSED:
            self.windowEditFamily.close()
            self.estado = 'base'

            if self.restartWinBase:
                self.windowBase.close()
                self.windowBase = itf.layoutBase(self.familiasList)

        if self.win == self.windowEditFamily and self.event == 'defPagante':
            self.famToEdit.pagante = self.value['defPagante']
            self.restartWinBase = True
        
        elif self.win == self.windowEditFamily and self.event == 'delPart':
            removedDias, removedValor = int(), float()
            
            removedParts =  self.dataManager.delElements(self.famToEdit.partsList, self.windowEditFamily)

            for p in removedParts:
                removedDias += int(p.dias)
                removedValor += float(p.pagou)
            self.InfoCalcsManager.attValuesViagem(removedDias, removedValor, sum=False)

            self.dataManager.attValuesFamilys(self.familiasList, self.InfoCalcsManager.valorPorDia)
                            
            self.windowEditFamily.close()
            self.windowEditFamily = itf.layoutEditFamily(self.famToEdit)
        
        elif self.win == self.windowEditFamily and self.event == 'addPart':
            
            self.windowAddEditPart = itf.layoutAddEditPart(func=False)
            
            self.estado = 'addEditPart'
            self.estadoBefore = 'editFam'

        for part in self.famToEdit.partsList[:]:
            
            if self.win == self.windowEditFamily and self.event == f'Pe{part.id}':
                self.windowAddEditPart = itf.layoutAddEditPart(part)
                self.partToEdit = part
                self.nomePart = f'{part.nome}'

                self.estado = 'addEditPart'
                self.estadoBefore = 'editFam'
        
        #for f in range(len(self.familiasList)):
        #    if self.familiasList[f].id == self.famToEdit.id:
        #        self.familiasList[f] = self.famToEdit

    def addEditPart(self):
        if self.win == self.windowAddEditPart and self.event == sg.WIN_CLOSED:
            self.windowAddEditPart.close()
            self.estado = self.estadoBefore

        elif self.win == self.windowAddEditPart and self.event == 'editPart':
            
            if self.dataManager.verificarInfoPart(self.value['partValor'], self.value['partDias']):

                valorBefore = float(self.partToEdit.pagou)
                diasBefore = int(self.partToEdit.dias)

                self.partToEdit.nome = self.value['partNome']
                self.partToEdit.pagou = self.value['partValor']
                self.partToEdit.dias = self.value['partDias']

                self.InfoCalcsManager.attValuesViagem(
                    diasBefore - int(self.partToEdit.dias),
                    valorBefore - float(self.partToEdit.pagou),
                    sum = False
                )

                self.dataManager.attValuesFamilys(self.familiasList, self.InfoCalcsManager.valorPorDia)

                self.windowAddEditPart.close()
                
                if self.estadoBefore == 'editFam':
                    
                    if self.nomePart == self.famToEdit.pagante:
                        self.famToEdit.pagante = self.partToEdit.nome

                    self.windowBase.close()
                    self.windowBase = itf.layoutBase(self.familiasList)
                    
                    self.windowEditFamily.close()
                    self.windowEditFamily = itf.layoutEditFamily(self.famToEdit)
                    self.estado = 'editFam'

            else:
                sg.popup("Por favor insira um número válido!", title="Erro", modal=True)
        
        elif self.win == self.windowAddEditPart and self.event == 'addPart':
            
            if self.dataManager.verificarInfoPart(self.value['partValor'], self.value['partDias']):
                
                self.dataManager.createPart(
                    
                    self.value['partNome'],
                    self.value['partValor'],
                    self.value['partDias'],
                    len(self.famToEdit.partsList),
                    self.famToEdit.partsList

                )

                partInfo = self.famToEdit.partsList[-1]
                
                self.InfoCalcsManager.attValuesViagem(partInfo.dias, partInfo.pagou)
                self.dataManager.attValuesFamilys(self.familiasList, self.InfoCalcsManager.valorPorDia)

                self.windowAddEditPart.close()
                

                if self.estadoBefore == 'editFam':
                    self.windowEditFamily.close()
                    self.windowEditFamily = itf.layoutEditFamily(self.famToEdit)

                    #self.windowEditFamily.find_element('defPagante').update(values=[part.nome for part in self.famToEdit.partsList])
                    #self.windowEditFamily.extend_layout(self.windowEditFamily['framePartEditFam'], [[sg.Text(partInfo.id), sg.Text(f'{partInfo.nome}, R${partInfo.pagou} Dias: {partInfo.dias}'), sg.Button('Editar', key=f'Pe{partInfo.id}'), sg.Checkbox('', key=partInfo.id)]])

                    self.estado = self.estadoBefore

            else:
                sg.popup("Por favor insira um número válido!", title="Erro", modal=True)

    def mainLoop(self):
        self.win, self.event, self.value = sg.read_all_windows()
        self.dataManager = dm.dataManager(self.event, self.value, self.win)

        if self.win == self.windowBase and self.event == sg.WIN_CLOSED:
            print(self.InfoCalcsManager.totalDias)
            exit()

        match self.estado:
            case 'base':
                self.winBase()
            case 'addFam':
                self.addFams() 
            case 'editFam':
                self.editFam()
            case 'addEditPart':
                self.addEditPart()
