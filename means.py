import csv


class means:
    def __init__(self):
        file = open("measurements.csv", "r")
        self.data = list(csv.reader(file, delimiter=","))
        file.close()
        print(self.data)

    # def calculating(self):
    #     with open ("","r"):
    def csv(self):
        """Create CSV file of all data"""
        with open("mean_values.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
            for d, t, a in zip(
                self.distance_motor, self.scanlength, self.amplitude_envelope
            ):
                writer.writerow([d, t, a])


means()
