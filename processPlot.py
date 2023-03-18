# Import statements
import heartpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as py

# Read data from CSV and store in data frame
data = pd.read_csv('dataStore.csv')
print(data)

# Retrieve data
D = data.to_numpy();
t = D[:,0]
ECG = D[:,1]
PPG = D[:,2]
print(PPG)

# Removes first 5 data entries from arrays as contain incorrect data as sensor is setting up
t = t[5:]
ECG = ECG[5:]
PPG = PPG[5:]

#samplerate = heartpy.get_samplerate_mstimer(t)
#print(samplerate)


# Filtering Data to remove noise (currently not working for PPG)
#filteredECG = heartpy.remove_baseline_wander(ECG,200)
#filteredPPG = heartpy.remove_baseline_wander(PPG, 199.7)
#print(filteredPPG)



# Normalising PPG data
normalizedPPG = (PPG-PPG.min())/ (PPG.max() - PPG.min())
#print(normalizedPPG)



#print(filteredECG)
plt.plot(t, normalizedPPG)
#plt.xlim(t[100], max(t))
plt.show()