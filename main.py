# main.py -- put your code here!
import pycom # we need this module to control the LED
from machine import Pin
from mqtt import MQTTClient
from network import WLAN
import machine
import time
from network import Sigfox
import socket

pycom.heartbeat(False) # disable the blue blinking
p_in = Pin('G9', mode=Pin.IN, pull=Pin.PULL_DOWN)

pycom.rgbled(0x0000FF)

sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ2)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

pycom.rgbled(0xFF0000)

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)
wlan.connect("ssid", auth=(WLAN.WPA2, "password"), timeout=5000)

while not wlan.isconnected():  
    machine.idle()



client = MQTTClient("d:nome_organizacao:tipo_dispositivo:id_dispositivo", "nome_organizacao.messaging.internetofthings.ibmcloud.com",user="use-token-auth", password="senha_do_dispositivo", port=1883)

client.connect()

pycom.rgbled(0x00FF00)
try:
    while(True):
        print(".")
        if p_in()==1:
            print("Fall detection")
            client.publish(topic="iot-2/evt/event/fmt/json", msg="{\"event\":\"falldetection\",\"position\":\"-27.6007891, -48.5232135\"}")
            pycom.rgbled(0xFF4500)
            time.sleep(2)
            pycom.rgbled(0x0000FF)
            s.send('fall')
            time.sleep(5)
            pycom.rgbled(0x00FF00)
except KeyboardInterrupt:
    print('interrupted!')

