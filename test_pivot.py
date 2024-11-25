import csv
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import hilbert
import numpy as np
from scipy.interpolate import griddata
import pandas as pd

import os
import glob

# Empty lists
distance = []
time = []
amplitude_raw = []


#arg = int(input("arg(34400)="))
#number = int(arg / 43)


# Load data from files
for d in range(0, 215, 5):
    for _ in range(800):  # NUMBER Repeat distances = 800
        distance.append(d)
    with open(f'{d}.000000.txt') as file:
        for line in file:
            column = line.split()
            time.append(float(column[0]))  # Convert to float
            amplitude_raw.append(float(column[1]))  # Convert to float

# Hilbert transform for amplitude envelope
hilbert_amplitude = hilbert(amplitude_raw)
amplitude_envelope = np.abs(hilbert_amplitude)

df = pd.DataFrame({'distance': distance, 'time':time, "amplitude_envolope": amplitude_envelope})
print(df)

piv = pd.pivot_table(df, values="amplitude_envelope",index=["time"], columns=["distance"])

