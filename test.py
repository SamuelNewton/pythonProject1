import serial
import time
import matplotlib.pyplot as plt
import csv


# Defining port and baud rate
arduino_port = 'COM5'
baud = 57600

# CSV to store data
fileECG = 'ECGdata.csv'
filePPG = 'PPGdata.csv'

# Arrays to store data
ECGdata = []
PPGdata = []

# Connect to serial port
ser = serial.Serial(arduino_port, baud)
print('Connected to Arduino Port:' + arduino_port)


# Display data to terminal
while True:

    try:
        getData = ser.readline()
        dataString = str(getData, 'utf-8')
        data = dataString[0:][:-2]
        readings = data.split(',')
        print(data)

        ECGdata.append(readings)

    except:
        print('Keyboard interrupt')
        break



# Write data to CSV file
with open(fileECG, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(ECGdata)



