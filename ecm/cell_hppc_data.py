import numpy as np
import pandas as pd


class CellHppcData:
    """
    Data from HPPC battey cell test.
    """

    def __init__(self, path, all_data=False):
        """
        Initialize with path to HPPC data file.

        Parameters
        ----------
        path : str
            Path to HPPC data file.
        all_data : bool
            By default `all_data=False` will read only the section of HPPC
            data from the data file. When `all_data=True` then read all the
            data in the data file.

        Attributes
        ----------
        time : vector
            Time vector for HPPC battery cell test data [s]
        current : vector
            Current from HPPC battery cell during test [A]
        voltage : vector
            Voltage from HPPC battery cell during test [V]
        flags : vector
            Flags for start and stop events in the HPPC battery cell data [-]
        """
        df = pd.read_csv(path)

        if all_data:
            self.time = df['Time(s)'].values
            self.current = df['Current(A)'].values
            self.voltage = df['Voltage(V)'].values
            self.flags = df['Data'].fillna(' ').values
        else:
            time = df['Time(s)'].values
            current = df['Current(A)'].values
            voltage = df['Voltage(V)'].values
            flags = df['Data'].fillna(' ').values

            ids = np.where(flags == 'S')[0]
            self.time = time[ids[1]:]
            self.current = current[ids[1]:]
            self.voltage = voltage[ids[1]:]
            self.flags = flags[ids[1]:]

    def get_ids(self):
        """
        Find all indices in data that represent the `S` flag. Start and stop
        procedures in the experiment are depcited by the `S` flag.

        Returns
        -------
        ids : vector
            Indices of start and stop points in data.
        """
        ids = np.where(self.flags == 'S')[0]
        return ids

    def get_idq(self):
        """
        Find index in data represented by `Q` which signals end of experiment.

        Returns
        -------
        idq : int
            Index of final stop point in data.
        """
        idq = np.where(self.flags == 'Q')[0]
        return idq

    def get_idx(self):
        """
        Construct indices for equivalent circuit model. Indices are in the short
        pulse section of the HPPC data.

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
        Construct indices for estimating RC parameters. Indices are in the long
        HPPC section where constant discharge occurs.

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
