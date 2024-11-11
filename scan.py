import csv

distance = []
time = []
amplitude = []

for d in range(0, 215, 5):
    #5.000000
    distance.append(d)
    with open(f'{d}.000000.txt') as file:
        for line in file:
            column = line.split()
            time.append(column[0])
            amplitude.append(column[1])

print(time)
aantal = time.count('0.416480')
print(aantal)