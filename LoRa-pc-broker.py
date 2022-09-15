#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By  :
# Emilio Caudillo Gispert,
# Jorge Antonio Castilla Valdez, Bruno Sánchez García,
# Santiago Ortiz Suzarte
# Created Date: 09/09/2022
# version ='1.0'
# ---------------------------------------------------------------------------
"""
This python code reads the data contained in csv "datos_reto.csv"
Once the csv is read, the data is encoded into a json string and send by
serial protocol UART to a LoRa development board connected through an usb port
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import serial
import time
import json
from paho.mqtt import client as mqtt_client
import random

# ---------------------------------------------------------------------------


# Defining the broker's ip and port
broker = '192.168.0.119'
port_b = 1883

# Defining max length of the buffer

MAX_BUFF_LEN = 255

SETUP = False

port = None

# Read the time when the code starts running

prev = time.time()

# Defining a list with al the json dictionary keys we need to read

keys = ['g1', 'g2', 'i1', 'i2', 'i3', 'wv', 'b', 'w', 'tv', 'g', 'k', 'o', 'p']

# Each of the keys matches an MQTT Topic

topics = ["/Nav/GPS/La/", "/Nav/GPS/Lo/", "/Nav/IMU/Roll/", "/Nav/IMU/Pitch/", "/Nav/IMU/Yaw/",
          "/Col/Fill/", "/Col/Proc_w/", "/Col/Thresh_v/", "/Check/Gas/", "/Check/Km/",
          "/Check/Oil/", "/Check/w_Pre/"]

# Printing the topics

print(topics)

# Defining the MQTT client id
client_id = f'python-mqtt-{random.randint(0,1000)}'


# The function read_serial receives the buffer length and reads from port a string with determined chars
def read_ser(num_char=1):
    string = port.read(num_char)
    return string.decode()


# The function connect_mqtt establish a MQTT connection with the broker
def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print("Failed to connect, return code %d\n",rc)
    client = mqtt_client.Client(client_id)
    # Use in case it is desired to protect the MQTT broker with a password
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port_b)
    return client


# The function publish, receives the client, the topic and data to publish on topic
def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    # Informs through a print if the message was sent correctly
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


# The function run is the main function of the code
def run():
    # Connecting to the mqtt broker
    client = connect_mqtt()
    client.loop_start()

    while 1:

        try:
            # Attempts to receive a string through serial USB connection with LoRA
            string = read_ser(MAX_BUFF_LEN)
        except Exception as e:
            # Exception for failing serial reading
            print("Serial Error")

        try:
            # Attempts to decode json string into dictionary
            information = json.loads(string)
            # Ensure that the information from LoRa with ID 4 is being received
            if information['ID'] == 4:
                id = information['ID']
                # Iterates through all topics list
                for i in topics:
                    # for each topic, indexes the data in received dictionary according to the respective key
                    # Example: "g1" ---> "/Nav/GPS/La/"
                    pub_data = float(information[keys[topics.index(i)]])
                    # Publishing the data on the respective topic
                    publish(client, str(id)+str(i), pub_data)
                    print(i, pub_data)

        except Exception as e:
            # Exception for failing json load or MQTT publishing
            pass


if __name__ == '__main__':
    while not SETUP:
        try:
            # Attempts to establish a serial connection with the defined port
            port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Use on linux depending on /dev port
            # port = serial.Serial('COM7', 115200, timeout=1)  # Use on Windows depending on the COM used

        except:
            # In case, port is not found , informs that the port is not connected
            if time.time() - prev > 2:
                print("No serial detected, please plug your uControl")
                prev = time.time()

            if port is None:
                continue
            SETUP = True
        run()
