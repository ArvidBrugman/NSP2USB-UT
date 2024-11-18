import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.interpolate as griddata
distance = []
time = []
amplitude = []

for d in range(0, 215, 5):
    #5.000000
    for _ in range(2000): #change later to calculation
        distance.append(d)
    with open(f'{d}.000000.txt') as file:
        for line in file:
            column = line.split()
            time.append(column[0])
            amplitude.append(column[1])

with open('measurements.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
    for d, t, a in zip(distance, time, amplitude):
        writer.writerow([d, t, a])

# fig, ax = plt.subplots()
# amplitude_max = amplitude[0]
# amplitude_min = amplitude[0]
# for _ in amplitude:
#     if _ > amplitude_max:
#         _ = amplitude_max
#     if _< amplitude_min:
#         _ = amplitude_min

# c = ax.pcolormesh(time, distance, amplitude, cmap='RdBu', vmin=amplitude_min, vmax=amplitude_max)
# ax.set_title('pcolormesh')
# # set the limits of the plot to the limits of the data
# ax.axis([time.min(), time.max(), distance.min(), distance.max()])
# fig.colorbar(c, ax=ax)

# plt.show()

x = np.linspace(min(time), max(time), 86001)
y = np.linspace(min(distance), max(distance), 86001)
x, y = np.meshgrid(x, y)

z = griddata((time, distance), amplitude, (x, y), method = 'cubic')

print(z)
sns.heatmap(z)
plt.show()

# plt.imshow(csvfile, cmap='viridis')
# plt.colorbar()
# plt.show()