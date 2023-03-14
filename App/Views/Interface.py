import PySimpleGUI as sg

def frameLayoutPart():
    frameLayoutPart = [
        [sg.Text('Nome:'), sg.Input(key='partNome', size=(15,30), do_not_clear=False)],
        [sg.Text('Valor Gasto R$:'), sg.Input(key='partValor', size=(15,30), do_not_clear=False)],
        [sg.Text('Dias Passados:'), sg.Input(key='partDias', size=(15,30), do_not_clear=False)],
        [sg.Button('Adicionar Participante', key='addPart'), sg.Button('Remover Participante', key='delPart', visible=False)]
    ]

    return frameLayoutPart

def layoutBase(familiasList, ext=True):
    
    layoutBase = [
        [sg.Frame('Familias', [[]] if familiasList else [[sg.Text('As Famílias serão exibidas aqui!')]], expand_x=True, key='frameFamilias')],
        [sg.Button('Adicionar', key='add'), sg.Button('Remover', key='delFam')]
    ]
    window = sg.Window('Base', layoutBase, finalize=True)

    if ext:
        row = [[sg.Text(f'{fam.pagante} R$: {fam.gastoTotal}'), sg.Button('Editar', key=fam.id), sg.Checkbox('', key=f'Fd{fam.id}')] for i, fam in enumerate(familiasList, start=1)]
        window.extend_layout(window['frameFamilias'], row)

    return window

def layoutAddFamily(partsList):
    layoutAddFamily = [
        [sg.Frame('Participante', frameLayoutPart()), sg.Frame('Lista de Participantes', [[]], key='partsList', expand_x=True, expand_y=True)],
        [sg.Button('Cancelar', key='cancelAddFam'), sg.Button('Criar', key='addFamily'), sg.Text('Pagante:') ,sg.Combo([part.nome for part in partsList], key='defPagAddWin', size=(20, None))]
    ]

    window = sg.Window('Adicionar Familia', layoutAddFamily, finalize=True)

    parts = [[sg.Text(f'{i}'), sg.Text(f'{part.nome}, R${part.pagou} Dias: {part.dias}'), sg.Checkbox('', key=f'P{part.id}')] for i, part in enumerate(partsList)]
    window.extend_layout(window['partsList'], parts)

    return window

def layoutAddEditPart(part=None, func=True):
    defaultsTexts = [part.nome, part.pagou, part.dias, 'Enviar'] if func else ['', '', '', 'Adicionar']

    layoutSubmitPart = [
    [sg.Text('Nome:'), sg.Input(default_text=defaultsTexts[0], key='partNome', size=(15,30))],
    [sg.Text('Valor Gasto:'), sg.Input(default_text=defaultsTexts[1], key='partValor', size=(15,30))],
    [sg.Text('Dias Passados:'), sg.Input(default_text=defaultsTexts[2], key='partDias', size=(15,30))],
    [sg.Button(defaultsTexts[3], key = 'editPart' if func else 'addPart')]
    ]

    return sg.Window('Editar Participante', layoutSubmitPart, finalize=True)

def layoutEditFamily(famToEdit):
    layoutEditFamily = [
        [sg.Frame('Participantes', [[sg.Text(f'{i}'), sg.Text(f'{part.nome}, R$: {part.pagou} Dias: {part.dias} Custou: R${part.deve:.2f}'), sg.Button('Editar', key=f'Pe{part.id}'), sg.Checkbox('', key=part.id)] for i, part in enumerate(famToEdit.partsList, start=1)] if famToEdit.partsList else [[sg.Text('')]], key='framePartEditFam')],
        [sg.Frame('Pagante', [[sg.Combo([part.nome for part in famToEdit.partsList], key='defPagante', default_value=famToEdit.pagante, enable_events=True)]])],
        [sg.Button('Adicionar Participante', key='addPart'), sg.Button('Remover Participantes', key='delPart'), sg.Button('Confirmar', key='confEditFam')]
    ]
    
    return sg.Window('Editar Familia', layoutEditFamily, finalize=True)
