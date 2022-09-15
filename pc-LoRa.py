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
import csv

# ---------------------------------------------------------------------------

# Defining max length of the buffer

MAX_BUFF_LEN = 255

SETUP = False

port = None

# Read the time when the code starts running

prev = time.time()

# Defines the dictionary that contains the data
data = {'ID': 4, 'g1': 19.610976101035302, 'g2': -99.22898598680044, 'i1': 0, 'i2': 0, 'i3': 10, 'wv': 0.5,
        'b': 100, 'w': 9999, 'tv': 1300, 'g': 100, 'k': 10000, 'o': 100, 'p': 50}

# Defines a list that contains all the keys from the previous dictionary
keys = ['g1', 'g2', 'i1', 'i2', 'i3', 'wv', 'b', 'w', 'tv', 'g', 'k', 'o', 'p']

# Establish the port where the LoRA is connected
"""
IMPORTANT: This port may change whether the code is being run on Linux or Windows
As a the first argument of function serial.Serial(), the port where LoRa is connected must be placed
"""

# This is the main cycle of the code

while not SETUP:
    # If the port is not connected, the code will print "No serial detected" until the LoRa is connected
    try:
        #port = serial.Serial('/dev/ttyACM0', 115200, timeout=1) #Use on linux depending on /dev port
        port = serial.Serial('COM7', 115200, timeout=1)  #Use on windows depending on the COM used

    except:
        if time.time() - prev > 2:
            print("No serial detected, please plug your uControl")

            prev = time.time()

        if port is None:
            continue
        SETUP = True

    # The function write_ser receives the data that must be sent serially to the LoRA
    def write_ser(ser_char):
        ser_char = ser_char + '\n'
        port.write(ser_char.encode())

    # The csv with the test data is read and for each column (Excluding the header), the data is sent each 2 seconds

    with open('datos_reto.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:

            if row[0] != "GPSLat":
                for i in keys:
                    # For each row, each cell is saved in the respective dictionary variable
                    data[i] = row[keys.index(i)]

                t0 = time.time()

                while time.time() - t0 <= 10:
                    pass
                # The data with the dictionary is encoded as a json string
                compact_data = json.dumps(data)
                # Sending the json string serially to the LoRa and printing in python console what is being sent
                write_ser(compact_data)
                print(compact_data)
