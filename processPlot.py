# Import statements
import heartpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as py
from scipy.signal import find_peaks

# Read data from CSV and store in data frame
data = pd.read_csv('dataStore.csv')
print(data)

# Retrieve data
D = data.to_numpy();
t = D[:,0]
ECG = D[:,1]
PPG = D[:,2]

# Removes first 5 data entries from arrays as contain incorrect data as sensor is setting up
t = t[377:]
ECG = ECG[377:]
PPG = PPG[377:]

#samplerate = heartpy.get_samplerate_mstimer(t)
#print(samplerate)


# Filtering Data to remove noise (currently not working for PPG)
ECG = heartpy.remove_baseline_wander(ECG,200)


# Normalising PPG data
normalizedPPG = (PPG-PPG.min())/ (PPG.max() - PPG.min())

# Normalising ECG data
normalizedECG = (ECG-ECG.min())/ (ECG.max() - ECG.min())

# Finding peaks in PPG data
peaksPPG, _ = find_peaks(normalizedPPG, distance=100, prominence=0.2)

# Finding peaks in ECG data
peaksECG, _ = find_peaks(normalizedECG, distance=100)


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


