from tkinter import CENTER
from PySimpleGUI import Window, Text, Input, Push, Column, VSeparator, HSeparator, Button, Slider,Combo, Multiline,cprint,Ok
import serial #pip install PySerial
import time
import threading

mytime = 0
readInterface = 0
event="" 
values=""

slider01 = {'value':90,'sent':0,'serial':"S1",'msg':"",'resp':""}
slider02 = {'value':90,'sent':0,'serial':"S2",'msg':"",'resp':""}
slider03 = {'value':90,'sent':0,'serial':"S3",'msg':"",'resp':""}

timeoutSend = 0

layout_bot = [
    [Text("Escolha como gostaria de resolver:",auto_size_text= True), Combo(["RAG", "Euler", "DH"]), Push(),Button("Teste do Robô",enable_events=True, size=(12,1), key='add')],
]

layout_Pxyz = [
    [Push(),Push(),Text("Px:"), Input(size=(4,1), key="Px"),Push(),Push(),Text("Al:"),Input(size=(4,1), key="alfa"),Push(),Push(),Push(),Push()],
    [Push(),Push(),Text("Py:"), Input(size=(4,1), key="Py"),Push(),Push(),Text("be:"), Input(size=(4,1), key="beta"),Push(),Push(),Push(),Push()],
    [Push(),Push(),Text("Pz:"),Input(size=(4,1), key="Pz"),Push(),Push(),Text("ga:"), Input(size=(4,1), key="gama"),Push(),Push(),Push(),Push()],
]

layout_abg = [
    [Button("envio",enable_events=True, size=(12,1), key='add1')],
    [Button("envio2",enable_events=True, size=(12,1), key='add2')]
    
]

layout_slider = [
    [Text("teta 1:"),Multiline(size= (5,2)),Text("teta 2:"),Multiline(size= (5,2)),Text("teta 3:"),Multiline(size= (5,2)) ],
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

    global mytime, timeoutSend
    mytime +=1

    if timeoutSend:
        timeoutSend -=1
    
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

threading.Timer( 0.1, periodic).start()

while 1:
  
    event, values = window.read(timeout=5)
    if event is not None:
        if event == "slider_01":
            slider01["value"] = values["slider_01"]
            slider01["msg"] = "S1:"+str(int(slider01["value"]))
            slider01["resp"] = "E" + slider01["msg"]
            slider01["sent"] = writeSerial(slider01["msg"])
            timeoutSend = 15
            # print("slider_01:",slider01["value"])
        if event == "slider_02":
            slider02["value"] = values["slider_02"]
            slider02["msg"] = "S2:"+str(int(slider02["value"]))
            slider02["resp"] = "E" + slider02["msg"]
            slider02["sent"] = writeSerial(slider02["msg"])
            timeoutSend = 15
            # print("slider_02:",slider02["value"])
        if event == "slider_03":
            slider03["value"] = values["slider_03"]
            slider03["msg"] = "S3:"+str(int(slider03["value"]))
            slider03["resp"] = "E" + slider03["msg"]
            slider03["sent"] = writeSerial(slider03["msg"])
            timeoutSend = 15
            # print("slider_02:",slider03["value"])
    
    
    serialData = comPort.read_until().decode('utf-8').rstrip()

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





window.close()
