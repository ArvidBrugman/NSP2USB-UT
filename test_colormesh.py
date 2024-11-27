import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import pandas as pd

# Empty lists
distance = []
time = []
amplitude_raw = []


# Load data from files
for d in range(0, 213, 3):
    for _ in range(2000):  # Repeat distances = 800
        distance.append(d)
    with open(f'{d}.000000.txt') as file:
        for line in file:
            column = line.split()
            time.append(float(column[0]))  # Convert to float
            amplitude_raw.append(float(column[1]))  # Convert to float
            # if column[0] > "0.4.3000":
            #     break
                
print(len(np.arange(0, 213, 3)))
print(len(time))

# # Hilbert transform for amplitude envelope
hilbert_amplitude = hilbert(amplitude_raw)
amplitude_envelope = np.abs(hilbert_amplitude)

# Create DataFrame
df = pd.DataFrame({'distance': distance, 'time': time, 'amplitude_envelope': amplitude_envelope})

# Pivot data for 2D grid
pivot_table = df.pivot_table(values='amplitude_envelope', index='time', columns='distance')

# Extract 2D arrays
distance_values = pivot_table.columns.values  # X-axis
time_values = pivot_table.index.values  # Y-axis
amplitude_values = pivot_table.values  # Z-axis

# Plot with pcolormesh
fig, ax = plt.subplots(figsize=(10, 6))
mesh = ax.pcolormesh(time_values, distance_values, amplitude_values.T, shading='auto', cmap='viridis')
fig.colorbar(mesh, ax=ax, label='Amplitude Envelope (in mV)')
ax.set_xlabel('Time (in ms)')
ax.set_ylabel('Distance (in mm)')
ax.set_title('Amplitude Envelope over Distance and Time')
plt.show()
