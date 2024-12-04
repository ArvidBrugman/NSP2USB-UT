import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import hilbert


class heatmap_scan:
    def __init__(self):
        # Empty lists
        self.distance_motor = []
        self.amplitude_raw = []
        self.scanlength = []
        self.amplitude_around0 = []

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
            with open(f"{d}.000000.txt") as file:
                for line in file:
                    column = line.split()
                    self.scanlength.append(float(column[0]) * 1500)  # Convert to float
                    self.amplitude_raw.append(float(column[1]))  # Convert to float
                    self.distance_motor.append(d)

        mean_amplitude_raw = np.mean(self.amplitude_raw)

        for i in self.amplitude_raw:
            self.amplitude_around0.append(i - mean_amplitude_raw)

        # hilbert transformation of self.amplitude_raw
        hilbert_amplitude = hilbert(self.amplitude_around0)
        self.amplitude_envelope = np.abs(hilbert_amplitude)

    def heatmap(self):
        """Plot the heatmap using pcolormesh"""
        # Create DataFrame
        df = pd.DataFrame(
            {
                "self.distance_motor": self.distance_motor,
                "scanlength": self.scanlength,
                "amplitude_envelope": self.amplitude_envelope,
            }
        )

        # Pivot data for 2D grid
        pivot_table = df.pivot_table(
            values="amplitude_envelope",
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
        fig.colorbar(mesh, ax=ax, label="Amplitude Envelope (in mV)")
        ax.set_xlabel("Scanlength  (in mm)")
        ax.set_ylabel("Distance of motor (in mm)")
        ax.set_title("Amplitude Envelope over Distance and Time")
        plt.show()

    def csv_creator(self):
        """Create CSV file of all data"""
        with open("raw_values.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Distance(mm)", "Time(ms)", "Amptitude(mV)"])
            for d, t, a in zip(
                self.distance_motor, self.scanlength, self.amplitude_envelope
            ):
                writer.writerow([d, t, a])


plot = heatmap_scan()
plot.lists(3, folder="meas1")
plot.heatmap()
plot.csv_creator()
