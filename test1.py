import csv
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import hilbert
import numpy as np
from scipy.interpolate import griddata

import os
import glob

# Empty lists
distance = []
time = []
amplitude_raw = []


arg = int(input("arg="))
number = int(arg / 43)


# Load data from files
for d in range(0, 215, 5):
    for _ in range(number):  # Repeat distances = 800
        distance.append(d)
    with open(f'{d}.000000.txt') as file:
        for line in file:
            column = line.split()
            time.append(float(column[0]))  # Convert to float
            amplitude_raw.append(float(column[1]))  # Convert to float

# Hilbert transform for amplitude envelope
hilbert_amplitude = hilbert(amplitude_raw)
amplitude_envelope = np.abs(hilbert_amplitude)

# Convert to arrays
distance = np.array(distance)
time = np.array(time)
amplitude_envelope = np.array(amplitude_envelope)

# Create grid for interpolation
xi = np.linspace(min(time), max(time), 1000)  # High resolution for smoothness
yi = np.linspace(min(distance), max(distance), 1000)
xi, yi = np.meshgrid(xi, yi)

# Interpolate data
zi = griddata((time, distance), amplitude_envelope, (xi, yi), method='cubic')

# Plot using a vibrant colormap
plt.figure(figsize=(12, 8))
sns.heatmap(
    zi,
    cmap='plasma',  # Vibrant colormap
    xticklabels=False,  # Hide ticks for a cleaner look
    yticklabels=False,
    cbar_kws={'label': 'Amplitude Envelope (mV)'}
)
plt.xlabel("Time (ms)")
plt.ylabel("Distance (mm)")
plt.title("Heatmap of Amplitude Envelope with Plasma Colormap")
plt.show()
