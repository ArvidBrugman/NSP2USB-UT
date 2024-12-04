from NSP2USB-UT.heatmap_scan import heatmap_scan
import csv

class means:
    def __init__(self):
        heatmap_scan().lists(3)
        self.csv = heatmap_scan().csv_creator()
        print(self.csv)

    def calculating(self):
    
    def csv(self):
        """Create CSV file of all data"""
        with open("raw_values.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
            for d, t, a in zip(
                self.distance_motor, self.scanlength, self.amplitude_envelope
            ):
                writer.writerow([d, t, a])

means()