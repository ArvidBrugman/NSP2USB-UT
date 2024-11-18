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
amplitude_raw_int = [int(x) for x in amplitude_raw]
print (amplitude_raw_int)

amplitude_around0 = []
meanrawamplitude = sum(amplitude_raw)/ len(amplitude_raw)
print(meanrawamplitude)
for i in amplitude_raw:
    amplitude_around0.append(i - meanrawamplitude )


# hilbert transformation of amplitude_raw
hilbert_amplitude = hilbert(amplitude_around0)
amplitude_envelope = np.abs(hilbert_amplitude)

print(amplitude_envelope)
plt.plot(time, amplitude_envelope)
plt.plot(time, amplitude_envelope.real)
plt.plot(time, amplitude_envelope.imag)
plt.show()