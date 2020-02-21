import numpy as np
import pandas as pd


class PackUs06Data:
    """
    Battery pack data from US06 drive cycle test. This battery pack represents
    3 battery modules connected in series. Each battery module contains 4
    battery cells connected in a 2S-2P configuration.

    Battery pack module configuration:

       |            |     |            |     |            |
    ---|== Module ==|--*--|== Module ==|--*--|== Module ==|---
       |            |     |            |     |            |
    """

    def __init__(self, path, all_data=False):

        df = pd.read_csv(path, skiprows=17)

        if all_data:
            self.time = df['Total Time'].values
            self.current = df['Current'].values
            self.voltage = df['Voltage'].values
            self.temp_a1 = df['Temperature A1'].values
            self.temp_a2 = df['Temperature A2'].values
            self.temp_a3 = df['Temperature A3'].values
        else:
            time = df['Total Time'].values
            current = df['Current'].values
            voltage = df['Voltage'].values
            temp_a1 = df['Temperature A1'].values
            temp_a2 = df['Temperature A2'].values
            temp_a3 = df['Temperature A3'].values

            idx = np.where(time == 600)[0][0]
            self.time = time[0:idx + 1]
            self.current = current[0:idx + 1]
            self.voltage = voltage[0:idx + 1]
            self.temp_a1 = temp_a1[0:idx + 1]
            self.temp_a2 = temp_a2[0:idx + 1]
            self.temp_a3 = temp_a3[0:idx + 1]
