# Import statements
import heartpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as py
from scipy.signal import find_peaks


# Read data from CSV and store in data frame
data = pd.read_csv('Sam_Powerlab_Wet.csv')
#print(data)

# Retrieve data
D = data.to_numpy();
t = D[:,0]
ECG = D[:,2]
PPG = D[:,1]

# Removes first 5 data entries from arrays as contain incorrect data as sensor is setting up
#t = t[5:]
#ECG = ECG[5:]
#PPG = PPG[5:]

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
peaksPPG, _ = find_peaks(normalizedPPG, distance=100, prominence=0.05)

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

fig, ax = plt.subplots(3, 1)
fig.suptitle('PowerLab - Wet (Ag/AgCl) Electrodes', fontweight='bold')

# PPG Signal
ax[0].plot(t, normalizedPPG, label='Normalized Pulse Wave')
ax[0].set_title('Pulse Transducer Signal')
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Amplitude (arbitrary units)')
ax[0].set_xticks(np.arange(min(t), max(t+1), 1))
ax[0].grid()

# ECG Signal
ax[1].plot(t, normalizedECG, label='Normalized ECG')
ax[1].set_title('ECG Signal')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Amplitude (arbitrary units)')
ax[1].set_xticks(np.arange(min(t), max(t+1), 1))
ax[1].grid()

# Combined plot with peaks shown
ax[2].plot(t, normalizedPPG, label='Normalized Pulse Wave')
ax[2].scatter(peaksPPG/200, normalizedPPG[peaksPPG], color = 'r', s = 10, marker = 'x', label = 'Pulse Wave Systolic Peak')
ax[2].plot(t, normalizedECG, label='Normalized ECG')
ax[2].scatter(peaksECG/200, normalizedECG[peaksECG], color = 'b', s = 10, marker = 'x', label = 'ECG R Wave Peak')
ax[2].set_title('Combined ECG and Pulse Transducer Signals with peaks identified')
ax[2].set_xlabel('Time (s)')
ax[2].set_ylabel('Amplitude (arbitrary units)')
ax[2].set_xticks(np.arange(min(t), max(t+1), 1))
ax[2].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0 )
ax[2].grid()




plt.show()


