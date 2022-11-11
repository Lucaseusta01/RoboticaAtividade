from tkinter import CENTER
from PySimpleGUI import Window, Text, Input, Push, Column, VSeparator, HSeparator, Button, Slider,Combo, Multiline,cprint,Ok

layout_bot = [
    [Text("Escolha como gostaria de resolver:",auto_size_text= True), Combo(["RAG", "Euler", "DH"]), Push(),Button("Teste do Robô", size=(12,1), key='add')],
]

layout_Pxyz = [
    [Push(),Push(),Text("Px:"), Input(size=(4,1), key="Px"),Push(),Push(),Text("Al:"),Input(size=(4,1), key="alfa"),Push(),Push(),Push(),Push()],
    [Push(),Push(),Text("Py:"), Input(size=(4,1), key="Py"),Push(),Push(),Text("be:"), Input(size=(4,1), key="beta"),Push(),Push(),Push(),Push()],
    [Push(),Push(),Text("Pz:"),Input(size=(4,1), key="Pz"),Push(),Push(),Text("ga:"), Input(size=(4,1), key="gama"),Push(),Push(),Push(),Push()],
]

layout_abg = [
    [Button("envio", size=(12,1), key='add1')],
    [Button("envio2", size=(12,1), key='add2')]
    
]

layout_slider = [
    [Text("teta 1:"),Multiline(size= (5,2)),Text("teta 2:"),Multiline(size= (5,2)),Text("teta 3:"),Multiline(size= (5,2)) ],
    [Text("teta 1:"), Slider(range=(0,180),orientation="h",size=(32,20),default_value=0,key="slider_01")],
    [Text("teta 2:"), Slider(range=(0,180),orientation="h",size=(32,20),default_value=0,key="slider_02")],
    [Text("teta 3:"), Slider(range=(0,180),orientation="h",size=(32,20),default_value=0,key="slider_03")]  
    ]

layout = [[

    Column(layout_abg),
    Column(layout_Pxyz),
    VSeparator(),
    Column(layout_slider),
    HSeparator(), 
    layout_bot,

    ]]

window = Window(
    "Robótica",
    layout = layout
)


# event, values = window.read()
while 1:
    event, values = window.read(timeout=20)
    print("Event:",event)
    print("Values:",values)
    # print(window.read(timeout=20))
    window["slider_01"].update()


window.close()
