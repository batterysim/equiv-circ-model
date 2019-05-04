import numpy as np
import pandas as pd
from .battery_data import BatteryData


class HppcData(BatteryData):
    """
    HPPC data processed for equivalent circuit model development.
    """

    def __init__(self, path):
        """
        Initialize with path to HPPC data file.

        Parameters
        ----------
        path : str
            Path to HPPC data file.

        Attributes
        ----------
        time : vector
            Time vector for battery test data [s]
        current : vector
            Current from battery during test [A]
        voltage : vector
            Voltage from battery during test [V]
        data : vector
            Data flags from battery test [-]
        """
        df = pd.read_csv(path)
        time = df['Time(s)'].values
        current = df['Current(A)'].values
        voltage = df['Voltage(V)'].values
        data = df['Data'].fillna(' ').values

        ids = np.where(data == 'S')[0]
        self.time = time[ids[1]:]
        self.current = current[ids[1]:]
        self.voltage = voltage[ids[1]:]
        self.data = data[ids[1]:]

    def process_data(self):
        """
        Process original data for use with equivalent circuit model. The S-flag
        determines start and stop indices `ids` in the data. Data preceding the
        first start/stop point is removed and remaining data is assigned to
        class attributes.
        """
        ids = np.where(self.data == 'S')[0]
        self.time = self.time[ids[1]:]
        self.current = self.current[ids[1]:]
        self.voltage = self.voltage[ids[1]:]
        self.data = self.data[ids[1]:]
