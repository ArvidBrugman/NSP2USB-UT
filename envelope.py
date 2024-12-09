import csv
import matplotlib.pyplot as plt
from scipy.fftpack import *
from scipy.signal import hilbert
import numpy as np
#empty lists
distance = []
time = []
amplitude_raw = []

with open(f'{81}.000001.txt') as file:
    for line in file:
        column = line.split()
        time.append(column[0])
        amplitude_raw.append((column[1]))

        
# create csv file
amplitude_float = []
with open('measurements2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([ "Time(ms)", "Amptitude(mV)"])
    for t, a in zip(time, amplitude_raw):
        writer.writerow([t, a])
        amplitude_float.append(float(a))


amplitude_around0 = []
meanrawamplitude = sum(amplitude_float)/ len(amplitude_float)
for i in amplitude_float:
    amplitude_around0.append(i - meanrawamplitude )


# hilbert transformation of amplitude_raw
hilbert_amplitude = hilbert(amplitude_around0)
amplitude_envelope = np.abs(hilbert_amplitude)
fig,ax = plt.subplots(1)

plt.plot(time, amplitude_around0, color='blue', label='Origineel Signaal')
plt.plot(time, amplitude_envelope, color='orange', label='Envelop')
ax.set_xticklabels([])
ax.set_xticks([])
ax.set_title("Hilbert transformatie van amplitude-meetresultaten")
plt.xlabel('Tijd (ms)')
plt.ylabel('Amplitude (mV)')
plt.legend()
plt.show()