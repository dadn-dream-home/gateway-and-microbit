import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_ID =  ["humi", "temp", "fan", "lamp"]
AIO_USERNAME = "Guts99"
AIO_KEY = "aio_srig869x8HXGGMvdwLapWDW88l2a"

def  connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_ID :
        client.subscribe(feed)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):
    #print("Nhan du lieu: " + feed_id + payload)
    if(feed_id == "fan"):
        print("Nhan du lieu fan: " + payload)
        ser.write(("FAN:" + str(payload)).encode())
    if (feed_id == "lamp"):
        print("Nhan du lieu lamp: " + payload)
        ser.write(("LAMP:" + str(payload)).encode())

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB-SERIAL" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

ser = serial.Serial( port=getPort(), baudrate=115200)


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[0] == "TEMP":
        client.publish("temp", splitData[1])
    if splitData[2] == "HUMI":
        client.publish("humi", splitData[3])


mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

while True:
    readSerial()
    time.sleep(1)