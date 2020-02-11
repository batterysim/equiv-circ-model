import numpy as np
import pandas as pd


class ModuleHppcData:
    """
    Data from HPPC battery module test.
    """

    def __init__(self, path, all_data=False):
        """
        Initialize with path to HPPC battery module data file.

        Parameters
        ----------
        path : str
            Path to HPPC battery module data file.
        all_data : bool
            By default `all_data=False` will read only the section of HPPC
            data from the data file. When `all_data=True` then read all the
            data in the data file.

        Attributes
        ----------
        time : vector
            Time vector for HPPC battery module test data [s]
        current : vector
            Current from HPPC battery module during test [A]
        voltage : vector
            Voltage from HPPC battery module during test [V]
        temp_a1 : vector
            Temperature from HPPC battery module test data [°C]
        flags : vector
            Flags for start and stop events in the HPPC battery module data [-]
        """
        df = pd.read_csv(path, skiprows=17)

        if all_data:
            self.time = df['Total Time'].values
            self.current = df['Current'].values
            self.voltage = df['Voltage'].values
            self.temp_a1 = df['Temperature A1'].values
            self.flags = df['Data Acquisition Flag'].values
        else:
            time = df['Total Time'].values
            current = df['Current'].values
            voltage = df['Voltage'].values
            temp_a1 = df['Temperature A1'].values
            flags = df['Data Acquisition Flag'].values

            ids = np.where(flags == 'S')[0]
            start = ids[21]     # index for start of hppc data
            end = ids[76]       # index for end of hppc data

            self.time = time[start:end + 1]
            self.current = current[start:end + 1]
            self.voltage = voltage[start:end + 1]
            self.temp_a1 = temp_a1[start:end + 1]
            self.flags = flags[start:end + 1]

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
