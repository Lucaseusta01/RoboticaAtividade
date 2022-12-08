from tkinter import CENTER
from PySimpleGUI import Window, Text, Input, Push, Column, VSeparator, HSeparator, Button, Slider,Combo, Multiline,cprint,Ok
import PySimpleGUI as sg
import serial #pip install PySerial
import time
import threading
from calculosM import MatrixRob
from numpy import cos,sin


# px = 17.2*cos(60)+13.7*cos(20)*cos(60) - 13.7*sin(20)*sin(30)*sin(60)-8*sin(60)*cos(30)
# py = 17.2*sin(60)+13.7*sin(60)*cos(20)+8*cos(30)*cos(60)+13.7*sin(20)*sin(30)*cos(60)
# pz = 8*sin(30)-13.7*sin(20)*cos(30)+4

  
teta1 = 90
teta2 = 30
teta3 = 90

oldTeta2 = 0

calculando = MatrixRob()
calculando.teste()
# px,py,pz = calculando.cinematica_dir(0,90,0)
# px,py,pz = calculando.cinematica_dir(teta1,teta2,teta3)

updateInterface = 10
calcularPonto = 0
# print(calculando.cinematica_dir(0,0,0))

# print('px: {}; py: {}; pz: {};'.format(px, py, pz))
# input("....")
mytime = 0

event="" 
values=""

position = {'Px':0.0,'Py':0.0,'Pz':0.0}
angulo = {'alfa':0,'beta':0,'gama':0}

slider01 = {'value':90.0,'sent':0,'serial':"S1",'msg':"",'resp':""}
slider02 = {'value':90.0,'sent':0,'serial':"S2",'msg':"",'resp':""}
slider03 = {'value':90.0,'sent':0,'serial':"S3",'msg':"",'resp':""}
garra = {'value':"Open",'sent':0,'serial':"S3",'msg':"",'resp':""}

# slider01["value"] = teta1
# slider02["value"] = teta2
# slider03["value"] = teta3

timeoutSend = 0

layout_bot = [
    [Text("Escolha como gostaria de resolver:",auto_size_text=True,enable_events=True), Combo(["RAG", "Euler", "DH"],enable_events=True,key="metodo"), Push(),Button("Teste do Robô",enable_events=True, size=(12,1), key='add')],
]

layout_Pxyz = [
    [Push(),Push(),Text("Px:"), Input(size=(4,1), key="Px",enable_events=True,default_text=0),Push(),Push(),Text("Al:"),Input(size=(4,1), key="alfa",enable_events=True,default_text=0),Push(),Push(),Push(),Push()],
    [Push(),Push(),Text("Py:"), Input(size=(4,1), key="Py",enable_events=True,default_text=0),Push(),Push(),Text("be:"), Input(size=(4,1), key="beta",enable_events=True,default_text=0),Push(),Push(),Push(),Push()],
    [Push(),Push(),Text("Pz:"),Input(size=(4,1), key="Pz",enable_events=True,default_text=0),Push(),Push(),Text("ga:"), Input(size=(4,1), key="gama",enable_events=True,default_text=0),Push(),Push(),Push(),Push()],
]

layout_abg = [
    [Button("envio",enable_events=True, size=(12,1), key='add1')],
    [Button("envio2",enable_events=True, size=(12,1), key='add2')],
    [Button("Garra",enable_events=True, size=(12,1), key='add3')]
    
]

layout_slider = [
    # [Text("teta 1:"),Multiline(size= (5,2)),Text("teta 2:"),Multiline(size= (5,2)),Text("teta 3:"),Multiline(size= (5,2)) ],
    [Text("teta 1:"),Input(size=(4,1), key="teta1",enable_events=True,default_text=90),Text("teta 2:"),Input(size=(4,1), key="teta2",enable_events=True,default_text=90),Text("teta 3:"),Input(size=(4,1), key="teta3",enable_events=True,default_text=90) ],
    [Text("teta 1:"), Push(),Slider(range=(0,180),orientation="h",enable_events=True,size=(32,20),default_value=slider01["value"],key="slider_01")],
    [Text("teta 2:"), Push(),Slider(range=(0,180),orientation="h",enable_events=True,size=(32,20),default_value=slider02["value"],key="slider_02")],
    [Text("teta 3:"), Push(),Slider(range=(0,180),orientation="h",enable_events=True,size=(32,20),default_value=slider03["value"],key="slider_03")]  
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

#função para enviar dados pela serial
def writeSerial(msg):

    send1 = msg
    answer = "E"+msg
    msg = msg + "\r\n"
    dataByte = bytes(msg,'utf-8')

    comPort.write(dataByte)
    
    ret = 1
    erro = "Erro"

    if serialData.count(answer):
        ret = 0
        # break
    elif serialData.startswith(erro):
        ret = 2
        # break   

    if ret == 0:
        print("[Python] Enviado:",send1,"R:Ok!")
    elif ret == 1:
        # print("[Python] Enviado:",send1,"Sem respota do dispositivo!")
        ret = 1
    elif ret == 2:
        # print("[Python] Enviado:",send1," R:",serialData)
        ret = 2
    elif ret == 3:
        # print("[Python] Enviado:",send1," Erro desconhecido.")
        ret = 3
    return ret

def periodic():

    global mytime, timeoutSend, updateInterface
    mytime +=1

    if timeoutSend:
        timeoutSend -=1
    
    if updateInterface:
        updateInterface -=1
    
    threading.Timer(0.1, periodic).start()




#======= serial setup ==========
serialControl = True
gateNumber = 'COM7'
baudRate = 115200

while serialControl:
    print("Opening Serial Communication...")
    try:
        comPort = serial.Serial(gateNumber, int(baudRate),timeout=0.05)
        print("Open Serial Communication!\n")
        serialControl = False
    except serial.serialutil.SerialException:
        print("GateError opening Serial Communication!\n")
        gateNumber = input("Insert the COM port number:")
        gateNumber = 'COM' + gateNumber
        baudRate = input('Insert speed(bps):')
    except NameError:
        print("NameError opening Serial Communication!\n")
        gateNumber = input("Insert the COM port number:")
        gateNumber = 'COM' + gateNumber
        baudRate = input('Insert speed(bps):')
    except ValueError:
        print("ValueError opening Serial Communication!\n")
        gateNumber = input("Insert the COM port number:")
        gateNumber = 'COM' + gateNumber
        baudRate = input('Insert speed(bps):')

comPort.close()
comPort.open()
serialData = comPort.read_until().decode('utf-8').rstrip()

threading.Timer(0.1, periodic).start()

# slider01["value"] = values["slider_01"]
slider01["msg"] = "S1:"+str(int(slider01["value"]))
slider01["resp"] = "E" + slider01["msg"]
slider01["sent"] = writeSerial(slider01["msg"])


# slider02["value"] = values["slider_02"]
slider02["msg"] = "S2:"+str(int(slider02["value"]))
slider02["resp"] = "E" + slider02["msg"]
slider02["sent"] = writeSerial(slider02["msg"])

# slider03["value"] = values["slider_03"]
slider03["msg"] = "S3:"+str(int(slider03["value"]))
slider03["resp"] = "E" + slider03["msg"]
slider03["sent"] = writeSerial(slider03["msg"])

while 1:

    # tratamento dos eventos
    if event is not None:

        if updateInterface == 0:
            
            px,py,pz = calculando.cinematica_dir(a=slider01["value"],b=slider02["value"],c=slider03["value"])
            position["Px"] = px
            position["Py"] = py
            position["Pz"] = pz
            # oldTeta2 = slider02["value"]
            window.Element("Px").Update(round(position["Px"],1))
            window.Element("Py").Update(round(position["Py"],1))
            window.Element("Pz").Update(round(position["Pz"],1))
            updateInterface = 20
        
            

        #slider
        if event == "slider_01":
            slider01["value"] = values["slider_01"]
            slider01["msg"] = "S1:"+str(int(slider01["value"]))
            slider01["resp"] = "E" + slider01["msg"]
            slider01["sent"] = writeSerial(slider01["msg"])
            window.Element("teta1").Update(int(slider01["value"]))
            # window.Element("Px").Update((position["Px"]))
            timeoutSend = 15
            # print("slider_01:",slider01["value"])
        if event == "slider_02":
            slider02["value"] = values["slider_02"]
            slider02["msg"] = "S2:"+str(int(slider02["value"]))
            slider02["resp"] = "E" + slider02["msg"]
            slider02["sent"] = writeSerial(slider02["msg"])
            window.Element("teta2").Update(int(slider02["value"]))
            # window.Element("Py").Update((position["Py"]))
            timeoutSend = 15
            calcularPonto = 1
            # print("slider_02:",slider02["value"])
        if event == "slider_03":
            slider03["value"] = values["slider_03"]
            slider03["msg"] = "S3:"+str(int(slider03["value"]))
            slider03["resp"] = "E" + slider03["msg"]
            slider03["sent"] = writeSerial(slider03["msg"])
            window.Element("teta3").Update(int(slider03["value"]))
            # window.Element("Pz").Update((position["Pz"]))
            timeoutSend = 15
            # print("slider_02:",slider03["value"])




            
        #botão
        if event == "metodo":
            metodo = values["metodo"]
            print("Metodo:",metodo)
        if event == "add":
            print("Teste do Robô press")
        if event == "add1":
            print("Envio press")
        if event == "add2":
            print("Envio 2 press")
        if event == "add3":
            if garra["value"] == "Open":
                print("Abrir Garra")
                garra["value"] = "Close"
                garra["msg"] = "S4:0"
                garra["sent"] = writeSerial(garra["msg"])
            elif garra ["value"] == "Close":
                print("Fechar Garra")
                garra["value"] = "Open"
                garra ["msg"] = "S4:120"
                garra["sent"] = writeSerial(garra["msg"])

        #ponto
        if event == "Px":
            position["Px"] = values["Px"]
            print("Px:",position["Px"])
            window.Element("Px").Update(int(slider01["value"]))
        if event == "Py":
            position["Py"] = values["Py"]
            print("Py:",position["Py"])
        if event == "Pz":
            position["Pz"] = values["Pz"]
            print("Pz:",position["Pz"])
        
        #angulo
        if event == "alfa":
            angulo["alfa"] = values["alfa"]
            print("alfa",angulo["alfa"])
        if event == "beta":
            angulo["beta"] = values["beta"]
            print("beta",angulo["beta"])
        if event == "gama":
            angulo["gama"] = values["gama"]
            print("gama",angulo["gama"])

        #angulo
        if event == "teta1":
            print("Teta1")
        if event == "teta2":
            print("Teta2")
        if event == "teta3":
            print("Teta3")

    # caso a janela seja fechada
    if event is None:
        window.close()
    else:
        event, values = window.read(timeout=50)

    serialData = comPort.read_until().decode('utf-8').rstrip()

    # verificação da resposta
    if (timeoutSend == 0) and (slider01["sent"]!=0):
        # print(".")
        slider01["sent"] = writeSerial(slider01["msg"])
        timeoutSend = 10
    elif serialData.count(slider01["resp"]) and (slider01["sent"]!=0):
        # print("Ok")
        slider01["sent"]=0
        print("[Python] Enviado:",slider01["msg"],"R:Ok!")
    if (timeoutSend == 0) and (slider02["sent"]!=0):
        # print(".")
        slider02["sent"] = writeSerial(slider02["msg"])
        timeoutSend = 10
    elif serialData.count(slider02["resp"]) and (slider02["sent"]!=0):
        # print("Ok")
        slider02["sent"]=0
        print("[Python] Enviado:",slider02["msg"],"R:Ok!")
    if (timeoutSend == 0) and (slider03["sent"]!=0):
        # print(".")
        slider03["sent"] = writeSerial(slider03["msg"])
        timeoutSend = 10
    elif serialData.count(slider03["resp"]) and (slider03["sent"]!=0):
        # print("Ok")
        slider03["sent"]=0
        print("[Python] Enviado:",slider03["msg"],"R:Ok!")

    # elif (slider01["sent"]!=0):
    #     serialData = comPort.read_until().decode('utf-8').rstrip()
    #     if serialData.count(slider01["resp"]):
    #         print("Ok")
    #         slider01["sent"]=0