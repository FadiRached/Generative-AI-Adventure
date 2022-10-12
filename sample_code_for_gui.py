import PySimpleGUI as sg

sg.theme("LightGrey")
sg.set_options(font = ("Courier New", 8))

frame_1 = [[sg.Text('This is where you will write your story')], [sg.Text('', size = (20,10)), sg.InputText()], [sg.Submit()], ]
frame_2 = [[sg.Text('This is where the image will be generated !')], ]

layout = [
    [sg.Frame('', frame_1, pad = (0,5)),
     sg.Frame('', frame_2, pad = (0, (12,7)), key = 'Hide')],
]

window = sg.Window('Image Generator', layout, resizable=True)
event, values = window.read()
window.maximize()
window.close()



