import numpy as np
import pandas as pd


class ModulesData:
    """
    Modules data representing three Nissan Leaf modules connected in series.
    """

    def __init__(self, path):
        df = pd.read_csv(path, skiprows=17)
        self.time = df['Total Time'].values
        self.step = df['Step'].values
        self.current = df['Current'].values
        self.voltage = df['Voltage'].values
        self.charge = df['Amp Hours Charge'].values
        self.discharge = df['Amp Hours Discharge'].values
        self.power = df['Power']
        self.temp_a1 = df['Temperature A1'].values
        self.temp_a2 = df['Temperature A2'].values
        self.temp_a3 = df['Temperature A3'].values
        self.flag = df['Data Acquisition Flag']

    def process(self):
        """
        Process data for first 600 seconds.
        """

        idx = np.where(self.time == 600)[0][0]
        self.time = self.time[0:idx + 1]
        self.current = self.current[0:idx + 1]
        self.voltage = self.voltage[0:idx + 1]
