import numpy as np
import pandas as pd


class CellTemperatureData:
    """
    Battery cell temperature data from charge/discharge test.
    """

    def __init__(self, path, ti, tf):
        """
        Initialize with path to temperature data file.

        Parameters
        ----------
        path : str
            Path to HPPC or charge/discharge data file.

        Attributes
        ----------
        tc1 : vector
            Thermocouple one [°C]
        tc2 : vector
            Thermocouple one [°C]
        tc3 : vector
            Thermocouple one [°C]
        tc4 : vector
            Thermocouple one [°C]
        """
        df = pd.read_csv(path, header=None, sep='\t', usecols=[1, 2, 3, 4])
        self.tc1 = df[1]
        self.tc2 = df[2]
        self.tc3 = df[3]
        self.tc4 = df[4]
        self.tmax = np.max((df[1], df[2], df[3]), axis=0)
        self.tavg = np.mean((df[1], df[2], df[3]), axis=0)
        self.tmin = np.min((df[1], df[2], df[3]), axis=0)

        # time for temperature data acquisition, time recorded every 3 seconds
        self.time = np.arange(len(self.tc1)) * 3

        # indices for start and end of section from original data
        self.id0 = np.argmin(np.abs(ti - self.time))
        self.id1 = np.argmin(np.abs(tf - self.time))

    @classmethod
    def process(cls, path, ti, tf):
        """
        Process the original temperature data for one section. This section of
        data is used for model development.
        """
        data = cls(path, ti, tf)
        id0 = data.id0
        id1 = data.id1

        # use data from first section of original data, time is adjusted to
        # start at zero, if id0 = id1 then data is from 3C discharge test
        if id0 == id1:
            max_id = data.tc2.idxmax()
            data.time = data.time[:max_id + 1] - data.time[:max_id + 1][0]
            data.tc1 = data.tc1[:max_id + 1]
            data.tc2 = data.tc2[:max_id + 1]
            data.tc3 = data.tc3[:max_id + 1]
            data.tc4 = data.tc4[:max_id + 1]
            data.tmax = data.tmax[:max_id + 1]
            data.tavg = data.tavg[:max_id + 1]
            data.tmin = data.tmin[:max_id + 1]
        else:
            data.time = data.time[id0:id1 + 1] - data.time[id0:id1 + 1][0]
            data.tc1 = data.tc1[id0:id1 + 1]
            data.tc2 = data.tc2[id0:id1 + 1]
            data.tc3 = data.tc3[id0:id1 + 1]
            data.tc4 = data.tc4[id0:id1 + 1]
            data.tmax = data.tmax[id0:id1 + 1]
            data.tavg = data.tavg[id0:id1 + 1]
            data.tmin = data.tmin[id0:id1 + 1]

        return data
