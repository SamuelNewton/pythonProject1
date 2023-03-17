import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('dataStore.csv')
print(data)

# Retrieve data
D = data.to_numpy();
t = D[:,0]
ECG = D[:,1]
PPG = D[:,2]



plt.plot(t, ECG)
plt.xlim(t[100], max(t))
plt.show()