import csv
import matplotlib.pyplot as plt
from scipy.fftpack import *
from scipy.signal import hilbert
import numpy as np
#empty lists
distance = []
time = []
amplitude_raw = []

for d in range(0, 215, 5):
    #5.000000
    for _ in range(2000): #change later to calculation (68000 / 43)
        distance.append(d)
    with open(f'{d}.000000.txt') as file:
        for line in file:
            column = line.split()
            time.append(column[0])
            amplitude_raw.append(column[1])

# create csv file
with open('measurements.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
    for d, t, a in zip(distance, time, amplitude_raw):
        writer.writerow([d, t, a])
    
print(a)
# hilbet transformation of amplitude_raw
amplitude_mean = np.mean(a)
print(amplitude_mean)
hilbert_amplitude = hilbert(amplitude_raw)
amplitude_envelope = np.abs(hilbert_amplitude)
