import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import hilbert


class heatmap_scan:
    def __init__(self):
        # Empty lists

        self.amplitude = []
        self.avg_scanlength = []
        self.avg_amplitude_envelope = []
        self.avg_distance_motor = []

    def lists(self, stepsize):
        """Create lists of the data gotten from the scan in txt files

        Args:
            STEPSIZE(int): The stepsize in mm that is used for the data.

        Returns:
            list: Distance that the motor has covered
            list: Distance that the scan has covered
            list: Amplitude of signal with Hilbert transformation
        """

        for d in range(0, 210 + stepsize, stepsize):
            for meas in range(1, 6):
                with open(f"{d}.00000{meas}.txt") as file:
                    for line in file:
                        self.distance_motor = []
                        self.amplitude_raw = []
                        self.scanlength = []
                        column = line.split()

                        self.scanlength.append(
                            float(column[0]) * 1500
                        )  # Convert to float
                        self.amplitude_raw.append(float(column[1]))
                        # hilbert transformation of self.amplitude_raw
                        hilbert_amplitude = hilbert(self.amplitude_around0)
                        self.amplitude_envelope = np.abs(
                            hilbert_amplitude
                        )  # Convert to float
                        self.distance_motor.append(d)
                        self.avg_scanlength.append(np.mean(self.scanlength))
                        self.avg_amplitude_envelope.append(
                            np.mean(self.amplitude_envelope)
                        )
                        self.avg_distance_motor.append(np.mean(self.distance_motor))

        # mean_amplitude_raw = np.mean(self.amplitude_raw)

        # for i in self.amplitude_raw:
        #     self.amplitude_around0.append(i - mean_amplitude_raw)

        mean_ampl = np.mean(self.avg_amplitude_envelope)
        for i in self.avg_amplitude_envelope:
            self.amplitude.append(i - mean_ampl)

    def heatmap(self):
        """Plot the heatmap using pcolormesh"""
        # Create DataFrame
        df = pd.DataFrame(
            {
                "self.distance_motor": self.avg_distance_motor,
                "scanlength": self.avg_scanlength,
                "amplitude": self.amplitude,
            }
        )
        print(df)
        # Pivot data for 2D grid
        pivot_table = df.pivot_table(
            values="amplitude",
            index="scanlength",
            columns="self.distance_motor",
        )

        # Extract 2D arrays
        distance_motor_values = pivot_table.columns.values  # X-axis
        distance_reflection_values = pivot_table.index.values  # Y-axis
        amplitude_values = pivot_table.values  # Z-axis

        # Plot with pcolormesh
        fig, ax = plt.subplots(figsize=(10, 6))
        mesh = ax.pcolormesh(
            distance_reflection_values,
            distance_motor_values,
            amplitude_values.T,
            shading="gouraud",
            cmap="seismic",
        )
        fig.colorbar(mesh, ax=ax, label="Amplitude (in mV)")
        ax.set_xlabel("Scanlength  (in mm)")
        ax.set_ylabel("Distance of motor (in mm)")
        ax.set_title("Amplitude over Distance and Time")
        plt.show()

    def csv_creator(self):
        """Create CSV file of all data"""
        with open("raw_values.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
            for d, t, a in zip(self.distance_motor, self.scanlength, self.amplitude):
                writer.writerow([d, t, a])


plot = heatmap_scan()
plot.lists(3)
plot.heatmap()
plot.csv_creator()
