import csv
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import hilbert
import numpy as np
from scipy.interpolate import griddata

import os
import glob


# folder_path = '\Users\study\Documents\GitHub\NSP2USB-UT\measurements1'
# for filename in glob.glob(os.path.join(folder_path, '*.txt')):
#     with open (filename, 'r') as file:
#         print(file.read())

# Empty lists
distance = []
time = []
amplitude_raw = []

# Load data from files
for d in range(0, 215, 5):
    for _ in range(2000):  # Repeat distances
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
xi = np.linspace(min(time), max(time), 500)  # High resolution for smoothness
yi = np.linspace(min(distance), max(distance), 100)
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
