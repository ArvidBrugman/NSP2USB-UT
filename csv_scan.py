import csv

amplitude_float = []
with open('raw_values.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
    for d, t, a in zip(motor_distance, scanlength, amplitude_raw):
        writer.writerow([d, t, a])
        amplitude_float.append(float(a))
