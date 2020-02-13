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

            # time vector is scaled to begin at 0, this helps when calculating curve fit coefficients
            ids = np.where(flags == 'S')[0]
            self.time = time[ids[1]:] - time[ids[1]]
            self.current = current[ids[1]:]
            self.voltage = voltage[ids[1]:]
            self.flags = flags[ids[1]:]

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

    def get_indices_q(self):
        """
        Find index in data represented by `Q` which signals end of experiment.

        Returns
        -------
        idq : int
            Index of final stop point in data.
        """
        idq = np.where(self.flags == 'Q')[0]
        return idq

    def get_indices_pulse(self):
        """
        Indices representing short pulse section in the HPPC battery cell
        data. Indices are given for each 10% SOC section.

        Returns
        -------
        id0 : ndarray
            Indices at start of pulse discharge for each 10% SOC section.
        id1 : ndarray
            Indices at time step after pulse discharge starts for each 10% SOC section.
        id2 : ndarray
            Indices at end of pulse discharge for each 10% SOC section.
        id3 : ndarray
            Indices at time step after pulse discharge ends for each 10% SOC section.
        id4 : ndarray
            Indices at end of pulse discharge rest period for each 10% SOC section.
        """
        ids = self.get_indices_s()
        id0 = ids[0::5]
        id1 = id0 + 1
        id2 = ids[1::5]
        id3 = id2 + 1
        id4 = ids[2::5]
        return id0, id1, id2, id3, id4

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
        id0 = ids[3::5][:-1]
        id1 = id0 + 1
        id2 = ids[4::5]
        id3 = id2 + 1
        id4 = ids[5::5]
        return id0, id1, id2, id3, id4
