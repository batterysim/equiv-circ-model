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
        df = pd.read_csv(path, skiprows=20)

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

            # scale time vector to begin at 0, this helps when calculating curve fit coefficients
            self.time = time[start:end + 1] - time[start]
            self.current = current[start:end + 1]
            self.voltage = voltage[start:end + 1]
            self.temp_a1 = temp_a1[start:end + 1]
            self.flags = flags[start:end + 1]

    def get_indices_s(self):
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

    def get_indices_discharge(self):
        """
        Indices representing long discharge section where constant discharge
        occurs in the HPPC battery cell data. Indices are given for each 10%
        SOC section.

        Returns
        -------
        id0 : ndarray
            Indices at start of constant discharge for each 10% SOC section.
        id1 : ndarray
            Indices at time step after constant discharge starts for each 10% SOC section.
        id2 : ndarray
            Indices at end of constant discharge for each 10% SOC section.
        id3 : ndarray
            Indices at time step after constant discharge ends for each 10% SOC section.
        id4 : ndarray
            Indices at end of constant discharge rest period for each 10% SOC section.
        """
        ids = self.get_indices_s()
        id0 = ids[0::6]
        id1 = id0 + 1
        id2 = ids[1::6]
        id3 = np.delete(id2, -1)
        id3 = id3 + 1
        id4 = ids[2::6]
        return id0, id1, id2, id3, id4
