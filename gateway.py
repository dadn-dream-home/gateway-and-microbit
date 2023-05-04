import serial.tools.list_ports
import random
import time
import  sys
import paho.mqtt.client as mqtt

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = ["humi", "temp", "fan", "led"]

def  connected(client, userdata, flags, rc):
    print("Ket noi thanh cong...")
    for feed in mqtt_topic :
        client.subscribe(feed)


def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client, userdata, msg):
    #print("Nhan du lieu: " + feed_id + payload)
    if(msg.topic == "fan"):
        print("Nhan du lieu fan: " + msg.payload)
        ser.write(("FAN:" + str(msg.payload)).encode())
    if (msg.topic == "lamp"):
        print("Nhan du lieu lamp: " + msg.payload)
        ser.write(("LAMP:" + str(msg.payload)).encode())

client = mqtt.Client()
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.connect(mqtt_broker, mqtt_port, 60)

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

client.loop_start()

while True:
    readSerial()
    time.sleep(1)