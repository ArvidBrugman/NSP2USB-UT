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
        all_ampl = []
        for a in range(0, 210 + stepsize, stepsize):
            for meas in range(1, 6):
                with open(f"{a}.00000{meas}.txt") as file:
                    for line in file:
                        column = line.split()
                        all_ampl.append(float(column[1]))

        mean_ampl = np.mean(all_ampl)

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
                        self.amplitude_raw.append(float(column[1]) - mean_ampl)
                        # hilbert transformation of self.amplitude_raw
                        hilbert_amplitude = hilbert(self.amplitude_raw)
                        self.amplitude_envelope = np.abs(
                            hilbert_amplitude
                        )  # Convert to float
                        self.distance_motor.append(d)
                        self.avg_scanlength.append(np.mean(self.scanlength))
                        self.amplitude.append(np.mean(self.amplitude_envelope))
                        self.avg_distance_motor.append(np.mean(self.distance_motor))

        error_amplitudie = np.std(self.amplitude) / np.sqrt(5)
        print(error_amplitudie)

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
            cmap="plasma",
        )
        fig.colorbar(mesh, ax=ax, label="Amplitude (in mV)")
        ax.set_xlabel("Afstand afgelegd door het signaal  (in mm)")
        ax.set_ylabel("Afstand afgelegd door motor (in mm)")
        ax.set_title("Amplitude van signaal over de afstand van de motor en de afstand afgelegd door het signaal")
        plt.show()

    def csv_creator(self):
        """Create CSV file of all data"""
        with open("raw_values.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
            for d, t, a in zip(self.avg_distance_motor, self.avg_scanlength, self.amplitude):
                writer.writerow([d, t, a])


plot = heatmap_scan()
plot.lists(3)
plot.heatmap()
plot.csv_creator()
