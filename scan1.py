import csv
import matplotlib.pyplot as plt
from scipy.fftpack import *
from scipy.signal import hilbert
import numpy as np
from scipy.interpolate import griddata
import os
#empty lists
distance = []
time = []
amplitude_raw = []


for d in range(0, 215, 5):
    #5.000000 = significance
    for _ in range(2000): #reoccur distances as there are muliple values per one distance
        #change later to calculation (68000 / 43)
        distance.append(d)
    with open(f'{d}.000000.txt') as file:
        for line in file:
            column = line.split()
            time.append(column[0])
            amplitude_raw.append(column[1])

# create csv file
amplitude_float = []
with open('raw_values.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
    for d, t, a in zip(distance, time, amplitude_raw):
        writer.writerow([d, t, a])
        amplitude_float.append(float(a))

# transform amplitudes around 0
amplitude_around0 = []
# calculate mean
meanrawamplitude = sum(amplitude_float)/ len(amplitude_float) 
for i in amplitude_float:
    # substract mean from each amplitude
    amplitude_around0.append(i - meanrawamplitude )

# hilbet transformation of amplitude_raw
amplitude_mean = np.mean(amplitude_float)
hilbert_amplitude = hilbert(amplitude_raw)
amplitude_envelope = np.abs(hilbert_amplitude)

# create csv file with hilbert amplitudes
with open('hilbert_values.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Distance(mm)", "Time(ms)", "Hilbert Amptitude(mV)"])
    for d, t, e in zip(distance, time, amplitude_envelope):
        writer.writerow([d, t, e])
print(min(distance), max(distance))
print(min(time), max(time))
# generate 5 evenly spaced numbers between min and max
x = np.linspace(min(distance), max(distance), 0.1)
print(x)
# x = np.linspace(min(time), max(time), 5)
# y = np.linspace(min(distance), max(distance), 5)
y = np.linspace(0, 100, 5)
x, y = np.meshgrid(x, y)

z = griddata((time, distance), amplitude_envelope, (x, y), method='cubic')

plt.imshow(z)
plt.show()



