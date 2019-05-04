import numpy as np
import pandas as pd


class BatteryData:
    """
    Battery cell data from HPPC or charge/discharge test.
    """

    def __init__(self, path):
        """
        Initialize with path to data file.

        Parameters
        ----------
        path : str
            Path to HPPC or charge/discharge data file.

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
        self.time = df['Time(s)'].values
        self.current = df['Current(A)'].values
        self.voltage = df['Voltage(V)'].values
        self.data = df['Data'].fillna(' ').values

    def get_ids(self):
        """
        Find indices in data that represented by the `S` flag. Start and stop
        procedures in the experiment are depcited by the `S` flag.

        Returns
        -------
        ids : vector
            Indices of start and stop points in data.
        """
        ids = np.where(self.data == 'S')[0]
        return ids

    def get_idq(self):
        """
        Find index in data represented by `Q` which signals end of experiment.

        Returns
        -------
        idq : int
            Index of final stop point in data.
        """
        idq = np.where(self.data == 'Q')[0]
        return idq

    def get_idx(self):
        """
        Construct indices for equivalent circuit model.

        Returns
        -------
        id0, id1, id2, id3, id4 : tuple
            Indices used for equivalent circuit model development.
            id0 = start of pulse discharge
            id1 = time step after pulse discharge starts
            id2 = end of pulse discharge ends
            id3 = time step after pulse discharge ends
            id4 = end of pulse discharge rest period
        """
        ids = self.get_ids()
        id0 = ids[0::5]
        id1 = id0 + 1
        id2 = ids[1::5]
        id3 = id2 + 1
        id4 = ids[2::5]
        return id0, id1, id2, id3, id4

    def get_idrc(self):
        """
        Construct indices for estimating RC parameters.

        Returns
        -------
        id0, id1, id2, id3, id4 : tuple
            Indices used to determine RC parameters.
            id0 = start of constant discharge
            id1 = time step after constant discharge starts
            id2 = end of constant discharge
            id3 = time step after constant discharge ends
            id4 = end of rest period
        """
        ids = self.get_ids()
        id0 = ids[3::5][:-1]
        id1 = id0 + 1
        id2 = ids[4::5]
        id3 = id2 + 1
        id4 = ids[5::5]
        return id0, id1, id2, id3, id4
