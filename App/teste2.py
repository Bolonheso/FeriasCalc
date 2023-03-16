import PySimpleGUI as sg

layout = [
    [sg.Text('Selecione um arquivo')],
    [sg.Input(), sg.Input() ,sg.FileBrowse(), sg.Input(), sg.Input(), sg.FileBrowse()],
    [sg.OK(), sg.Cancel(), sg.Input()]
]

window = sg.Window('Selecionar arquivo', layout)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event == 'OK':
        arquivo_selecionado = values[0]
        prit(f'nO arquivo selecionado foi: {arquivo_selecionado}')

window.close()
