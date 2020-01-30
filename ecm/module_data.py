import pandas as pd


class ModuleData:
    """
    Battery module data.
    """

    def __init__(self, path):
        df = pd.read_csv(path, skiprows=17)
        self.time = df['Total Time'].values
        self.current = df['Current'].values
        self.voltage = df['Voltage'].values
        self.temp_a1 = df['Temperature A1'].values
        self.flag = df['Data Acquisition Flag'].values

    def process_data(self):
        """
        here
        """
