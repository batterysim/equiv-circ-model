import numpy as np
import pandas as pd


class CellDischargeData:
    """
    Battery cell data from discharge test.
    """

    def __init__(self, path):
        """
        Initialize with path to discharge data file.

        Parameters
        ----------
        path : str
            Path to discharge data file.

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
        dt : vector
            Time step [s]
        """
        df = pd.read_csv(path)
        self.time = df['Time(s)'].values
        self.current = df['Current(A)'].values
        self.voltage = df['Voltage(V)'].values
        self.data = df['Data'].fillna(' ').values
        self.ti = 0
        self.tf = 0

    def get_ids(self):
        """
        Find indices in data that represent the `S` flag. Start and stop
        procedures in the experiment are depicted by the `S` flag.

        Returns
        -------
        ids : vector
            Indices of start and stop points in data.
        """
        ids = np.where(self.data == 'S')[0]
        return ids

    def get_idx(self):
        """
        Find indices in discharge data that represent a single section.

        Returns
        -------
        id0, id1, id2, id3 : tuple
            Indices representing section of discharge data.
            id0 = start of discharge
            id1 = end of discharge
            id2 = start of charge
            id3 = end of charge
        """
        ids = self.get_ids()

        if max(abs(self.current)) > 35:
            # 2c and 3c discharge tests
            id0 = ids[3]
            id1 = ids[4]
            id2 = ids[5]
            id3 = ids[6]
        else:
            # 1c discharge test
            id0 = ids[2]
            id1 = ids[3]
            id2 = ids[4]
            id3 = ids[5]

        return id0, id1, id2, id3

    @classmethod
    def process(cls, path):
        """
        Process the original discharge data for one section. This section of
        data is used for model development.
        """
        data = cls(path)

        id0, id1, id2, id3 = data.get_idx()

        data.ti = data.time[id0]
        data.tf = data.time[id2]
        data.current = data.current[id0:id2 + 1]
        data.voltage = data.voltage[id0:id2 + 1]
        data.time = data.time[id0:id2 + 1] - data.time[id0:id2 + 1].min()

        return data

    @classmethod
    def process_discharge_only(cls, path):
        """
        Process the original discharge data for just the discharge portion.
        """
        data = cls(path)

        id0, id1, _, _ = data.get_idx()

        data.ti = data.time[id0]
        data.tf = data.time[id1]
        data.current = data.current[id0:id1 + 1]
        data.voltage = data.voltage[id0:id1 + 1]
        data.time = data.time[id0:id1 + 1] - data.time[id0:id1 + 1][0]

        return data
