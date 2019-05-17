import numpy as np
from scipy.optimize import curve_fit


class HppcEcm:
    """
    Equivalent circuit model (ECM) developed from HPPC battery cell data.
    """

    def __init__(self, hppc_data):
        """
        Initialize with the `HppcData` class object.

        Parameters
        ----------
        hppc_data : HppcData
            Data from the HPPC battery cell test. This parameter must be a class
            object of `HppcData`.
        """

        self.current = hppc_data.current
        self.time = hppc_data.time
        self.voltage = hppc_data.voltage
        self.idx = hppc_data.get_idx()
        self.idrc = hppc_data.get_idrc()

    def points(self, soc):
        """
        Method to get OCV related points in HPPC data and SOC vector.
        """

        id0 = self.idx[0]
        i_pts = np.append(self.current[id0], self.current[-1])
        t_pts = np.append(self.time[id0], self.time[-1])
        v_pts = np.append(self.voltage[id0], self.voltage[-1])
        z_pts = np.append(soc[id0], soc[-1])
        return i_pts, t_pts, v_pts, z_pts

    def curve_fit_coeff(self, func, ncoeff):
        """
        Determine curve fit coefficients for each 10% change in SOC from HPPC
        data. These coefficients are used to calculate the RC parameters.

        Parameters
        ----------
        func : function
            Exponential function defining the curve.
        ncoeff : int
            Number of coefficients in the exponential function.

        Returns
        -------
        coeff : array
            Coefficients at each 10% change in SOC.
        """

        _, _, id2, _, id4 = self.idrc
        nrow = len(id2)
        coeff = np.zeros((nrow, ncoeff))

        for i in range(nrow):
            start = id2[i]
            end = id4[i]
            t_curve = self.time[start:end]
            v_curve = self.voltage[start:end]
            t_scale = t_curve - t_curve[0]
            if ncoeff == 3:
                guess = v_curve[-1], 0.01, 0.01
            elif ncoeff == 5:
                guess = v_curve[-1], 0.01, 0.01, 0.001, 0.01
            popt, pcov = curve_fit(func, t_scale, v_curve, p0=guess)
            coeff[i] = popt

        return coeff

    def rctau_ttc(self, coeff):
        """
        Determine tau, resistor, and capacitor values (RC parameters) for each
        10% change in SOC from HPPC data.

        Parameters
        ----------
        coeff : array
            Coefficients at each 10% change in SOC from HPPC data.

        Returns
        -------
        rctau : array
            RC parameters as determined from HPPC data. Each row is for a 10%
            change in SOC. For example, RC parameters for SOC 100-90% is
            rctau[0] = tau1, tau2, r0, r1, r2, c1, c2 where
            tau1 : float
                First time constant [s]
            tau2 : float
                Second time constant [s]
            r0 : float
                Series resistance [Ω]
            r1 : float
                Resistance in first RC branch [Ω]
            r2 : float
                Resistance in second RC branch [Ω]
            c1 : float
                Capacitance in first RC branch [F]
            c2 : float
                Capacitance in second RC branch [F]
        """

        id0, id1, id2, _, _, = self.idrc
        nrow = len(id0)
        rctau = np.zeros((nrow, 7))

        for k in range(nrow):
            di = abs(self.current[id1[k]] - self.current[id0[k]])
            dt = self.time[id2[k]] - self.time[id0[k]]
            dv = abs(self.voltage[id1[k]] - self.voltage[id0[k]])

            _, b, c, alpha, beta = coeff[k]

            tau1 = 1 / alpha
            tau2 = 1 / beta
            r0 = dv / di
            r1 = b / ((1 - np.exp(-dt / tau1)) * di)
            r2 = c / ((1 - np.exp(-dt / tau2)) * di)
            c1 = tau1 / r1
            c2 = tau2 / r2

            rctau[k] = tau1, tau2, r0, r1, r2, c1, c2

        return rctau

    @staticmethod
    def func_otc(t, a, b, alpha):
        """
        Exponential function for a one time constant model (OTC).
        """
        return a - b * np.exp(-alpha * t)

    @staticmethod
    def func_ttc(t, a, b, c, alpha, beta):
        """
        Exponential function for a two time constants model (TTC).
        """
        return a - b * np.exp(-alpha * t) - c * np.exp(-beta * t)
