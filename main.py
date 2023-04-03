# Import statements
import serial
import time
import csv
import heartpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as py
from scipy.signal import find_peaks

port = 'COM5'
baud = 115200
k = 0

f = open('dataStore.csv', 'w', newline='')
f.truncate()

serialCom = serial.Serial(port, baud)
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)

dataPoints = 2001

for k in range(dataPoints):
    try:
        s_bytes = serialCom.readline()
        decoded_bytes = s_bytes.decode('utf-8').strip('\r\n')
        #print(decoded_bytes)

        if k == 0:
            values = decoded_bytes.split(',')
        else:
            values = [float(x) for x in decoded_bytes.split()]
        print(values)

        writer = csv.writer(f, delimiter=',')
        writer.writerow(values)

    except:
        print('Error, not recorded')





# Read data from CSV and store in data frame
data = pd.read_csv('dataStore.csv')
#print(data)

# Retrieve data
D = data.to_numpy();
t = D[:,0]
ECG = D[:,1]
PPG = D[:,2]

# Removes first 5 data entries from arrays as contain incorrect data as sensor is setting up
t = t[5:]
ECG = ECG[5:]
PPG = PPG[5:]

#samplerate = heartpy.get_samplerate_mstimer(t)
#print(samplerate)

# Length of users arm from sternal notch to fingertip
#length = input("Enter length of arm in m: ")
length = 0.8

def average(PWV):
    return sum(PWV)/len(PWV)


# Filtering Data to remove noise (currently not working for PPG)
ECG = heartpy.remove_baseline_wander(ECG,200)


# Normalising PPG data
normalizedPPG = (PPG-PPG.min())/ (PPG.max() - PPG.min())

# Normalising ECG data
normalizedECG = (ECG-ECG.min())/ (ECG.max() - ECG.min())

# Finding peaks in PPG data
peaksPPG, _ = find_peaks(normalizedPPG, distance=100, prominence=0.1)

# Finding peaks in ECG data
peaksECG, _ = find_peaks(normalizedECG, distance=100, prominence=0.2)

print(peaksPPG)
print(peaksECG)

# Lists to store
PWV = [None] * len(peaksPPG)
sampleDiff = [None] * len(peaksPPG)
timeDiff = [None] * len(peaksPPG)

# Calculating time difference between peaks and hence PWV
for i in range(0, len(peaksPPG)):
    sampleDiff[i] = peaksPPG[i] - peaksECG[i]
    timeDiff[i] = sampleDiff[i] / 200
    PWV[i] = length / timeDiff[i];



print(sampleDiff)
print(timeDiff)
print(PWV)

averagePWV = average(PWV)
print("Average PWV of user is: ", averagePWV)


# Plotting
fig = plt.figure()
ax = fig.subplots(3)
# PPG Signal
ax[0].plot(normalizedPPG, label='Normalized PPG')
# ECG Signal
ax[1].plot(normalizedECG, label='Normalized ECG')

# Combined plot with peaks shown
ax[2].plot(normalizedPPG, label='Normalized PPG')
ax[2].scatter(peaksPPG, normalizedPPG[peaksPPG], color = 'r', s = 10, marker = 'x', label = 'PPG maxima')
ax[2].plot(normalizedECG, label='Normalized ECG')
ax[2].scatter(peaksECG, normalizedECG[peaksECG], color = 'b', s = 10, marker = 'x', label = 'ECG maxima')
ax[2].legend()
ax[2].grid()
plt.show()


