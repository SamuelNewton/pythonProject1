# Same functionality as processPlot.py however splitting into functions so they can be called from a GUI


# Import statements
import heartpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as py
from scipy.signal import find_peaks


# Read data from CSV and store in data frame
data = pd.read_csv('dataStore.csv')
#print(data)

#Input arg = list


# Retrieve data
D = data.to_numpy();
t = D[:,0]
ECG = D[:,1]
PPG = D[:,2]

# Removes first 5 data entries from arrays as contain incorrect data as sensor is setting up
t = t[5:]
ECG = ECG[5:]
PPG = PPG[5:]




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


def age():
    age = int(input("Enter your age: "))
    return age


def length():
    length = float(input("Enter length of arm in m: "))
    return length


def PWVcalc():  # Takes peaks from PPG and ECG data and returns an average PWV value
    # Lists to store PTT data and corresponding PWV values


    #

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
    # Returns average PWV value
    return sum(PWV) / len(PWV)


# Calling functions
length = length()
age = age()
print("Average PWV of user is: ", PWVcalc())


#if age >= 20 && age <= 29:
 #   print("Healthy range is 3 to 6")
#elif age >= 30 && age <= 39:
 #   print("Healthy range is 3 to 6")
#elif age >= 40 && age <= 49:
 #   print("Healthy range is 3 to 6")


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


