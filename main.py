import paho.mqtt.client as mqtt #import library
import subprocess
import os
import json
import requests
import base64
import multiprocessing
import random
import time
import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BOARD)

MQTT_SERVER = "hairdresser.cloudmqtt.com" #specify the broker address, it can be IP of raspberry pi or simply localhost
MQTT_PORT = 37670
MQTT_USERNAME = "knumunby"
MQTT_PASSWORD = "efG-FmGehi9G"

LED1 = 11
LED2 = 15
LED3 = 16

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)

TOPIC_BUTTON_1 = "bouton/1"
TOPIC_BUTTON_2 = "bouton/2"
TOPIC_BUTTON_3 = "bouton/3"

def is_cnx_active(timeout):
    """Cette fonction permet de détecter si la raspberry est connectée à l'internet"""

    try:
        requests.head("https://preset.herokuapp.com/", timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def wait_for_connection():
    """Cette fonction boucle tant qu'une connection à internet n'est pas active"""

    while True:
        if is_cnx_active(1) is True:
            # Do somthing
            print("The internet connection is active")
            break
        else:
            pass

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    """Callback appelé à la connection de la raspberry sur le serveur MQTT"""

    print("Connected with result code "+str(rc))

    client.subscribe(TOPIC_BUTTON_1)
    client.subscribe(TOPIC_BUTTON_2)
    client.subscribe(TOPIC_BUTTON_3)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    """Callback appelé lorsqu'un message est reçu sur un topic"""
    print(msg.topic+" "+str(msg.payload))

    if msg.topic == TOPIC_BUTTON_1:
        if str(msg.payload).find("play") != -1:
            print("play bouton1")
            GPIO.output(LED1, 1)
        elif str(msg.payload).find("stop") != -1:
            print("stop bouton1")
            GPIO.output(LED1, 0)
    elif msg.topic == TOPIC_BUTTON_2:
        if str(msg.payload).find("play") != -1:
            print("play bouton2")
            GPIO.output(LED2, 1)
        elif str(msg.payload).find("stop") != -1:
            print("stop bouton2")
            GPIO.output(LED2, 0)
    elif msg.topic == TOPIC_BUTTON_3:
        if str(msg.payload).find("play") != -1:
            print("play bouton3")
            GPIO.output(LED3, 1)
        elif str(msg.payload).find("stop") != -1:
            print("stop bouton3")
            GPIO.output(LED3, 0)

# if __name__ == '__main__':
wait_for_connection()
client = mqtt.Client(transport='websockets')
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=MQTT_USERNAME,password=MQTT_PASSWORD)
client.connect(MQTT_SERVER, MQTT_PORT)
client.loop_forever() #use this line if you don't want to write any further code. It blocks the code forever to check for data
# client.loop_start()  #use this line if you want to write any more code here
