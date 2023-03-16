import PySimpleGUI as sg

layout = [
    [sg.Frame("treeas", [[sg.Button("eae", key="botão"), sg.Button("-eae", key="-botão")]], key="frame")]
]

window = sg.Window('Selecionar arquivo', layout)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event == "botão": window.extend_layout(window['frame'], [[sg.Text("eae galerinha")]])
    elif event == "-botão": window['frame'].update([[sg.Button("eae", key="botão"), sg.Button("-eae", key="-botão")]])
    

window.close()

