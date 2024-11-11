import csv
import matplotlib.pyplot as plt

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


plt.scatter(time, distance)
plt.show()