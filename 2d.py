import csv
import matplotlib.pyplot as plt
from scipy.fftpack import *
from scipy.signal import hilbert
import numpy as np
#empty lists
distance = []
time = []
amplitude_raw = []

with open(f'{150}.000000.txt') as file:
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


print(amplitude_float)

amplitude_around0 = []
meanrawamplitude = sum(amplitude_float)/ len(amplitude_float)
print(meanrawamplitude)
for i in amplitude_float:
    amplitude_around0.append(i - meanrawamplitude )


# hilbert transformation of amplitude_raw
hilbert_amplitude = hilbert(amplitude_around0)
amplitude_envelope = np.abs(hilbert_amplitude)
print(amplitude_envelope[50:200])

plt.plot(time, amplitude_around0)
plt.plot(time, amplitude_envelope)
# plt.plot(time, amplitude_envelope.real)
# plt.plot(time, amplitude_envelope.imag)
plt.show()