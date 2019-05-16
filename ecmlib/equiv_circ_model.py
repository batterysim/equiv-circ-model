import numpy as np
from scipy.optimize import curve_fit


class EquivCircModel:
    """
    Equivalent circuit model (ECM).
    """

    def __init__(self, data, params):
        """
        Initialize with HppcData object and parameters module.

        Parameters
        ----------
        data : HppcData
            HPPC object containing time, current, voltage data.
        params : module
            Parameters for battery cell.

        Attributes
        ----------
        data : HppcData
            Object representing HPPC data.
        params : module
            Parameters module for battery cell.
        """
        self.data = data
        self.params = params

    @property
    def points(self):
        """
        Method to get OCV related points in HPPC data and SOC vector.
        """
        id0 = self.data.get_idx()[0]
        i_pts = np.append(self.data.current[id0], self.data.current[-1])
        t_pts = np.append(self.data.time[id0], self.data.time[-1])
        v_pts = np.append(self.data.voltage[id0], self.data.voltage[-1])
        soc_pts = np.append(self.soc[id0], self.soc[-1])
        return i_pts, t_pts, v_pts, soc_pts

    @property
    def soc(self):
        """
        State of charge (SOC).

        Calculate the state of charge of a battery cell using the method from
        Gregory Plett's book [#plett]. Fully charged is SOC=1 and fully
        discharged is SOC=0. SOC is also referred to as `z` in some texts.

        .. math:: \\frac{dz}{dt} = \\frac{-i(t)\\,\\eta(t)}{Q}

        Parameters
        ----------
        eta_chg : float
            Coulombic efficiency for charge, typically <= 1.0 [-]
        eta_dis : float
            Coulombic efficiency for discharge, typically = 1.0 [-]
        q : float
            Total capacity of battery cell [Ah]

        Returns
        -------
        z : vector
            State of charge at every time step in data [-]

        Note
        ----
        Battery cell capacity `q` is converted in this function from Ah to As.

        References
        ----------
        .. [#plett] Plett, Gregory L. Battery Management Systems, Volume I: Battery
           Modeling. Vol. 2. Artech House, 2015.
        """
        q = self.params.q_cell * 3600
        dt = np.diff(self.data.time)

        nc = len(self.data.current)
        z = np.ones(nc)

        for k in range(1, nc):
            i = self.data.current[k]
            if i > 0:
                eta = self.params.eta_chg
            else:
                eta = self.params.eta_dis
            z[k] = z[k - 1] + ((eta * i * dt[k - 1]) / q)

        return z

    @property
    def ocv(self):
        """
        Open circuit voltage (OCV).

        Linearly interpolate the open circuit voltage from state of charge
        points and voltage points in the HPPC data. Points are at 10% intervals
        of SOC. Returned OCV vector is same length as battery data used to
        determine SOC.

        Parameters
        ----------
        soc : vector
            State of charge for every time step in data [s]

        Returns
        -------
        ocv : vector
            Open circuit voltage for every time step in data [V]
        """
        _, _, v_pts, soc_pts = self.points
        ocv = np.interp(self.soc, soc_pts[::-1], v_pts[::-1])
        return ocv

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
        _, _, id2, _, id4 = self.data.get_idrc()
        nrow = len(id2)
        coeff = np.zeros((nrow, ncoeff))

        for i in range(nrow):
            start = id2[i]
            end = id4[i]
            t_curve = self.data.time[start:end]
            v_curve = self.data.voltage[start:end]
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
            Coefficients at each 10% change in SOC.

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
        id0, id1, id2, _, _, = self.data.get_idrc()
        nrow = len(id0)
        rctau = np.zeros((nrow, 7))

        for k in range(nrow):
            di = abs(self.data.current[id1[k]] - self.data.current[id0[k]])
            dt = self.data.time[id2[k]] - self.data.time[id0[k]]
            dv = abs(self.data.voltage[id1[k]] - self.data.voltage[id0[k]])

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

    def get_rtau(self, rctau, z):
        """
        Determine tau and resistor values for any SOC.
        """

        # determine index where z is close to soc parameters
        soc = np.arange(0.1, 1.0, 0.1)[::-1]
        idx = abs(soc - z).argmin()

        # return resistor and tau values at z
        tau1 = rctau[:, 0][idx]
        tau2 = rctau[:, 1][idx]
        r0 = rctau[:, 2][idx]
        r1 = rctau[:, 3][idx]
        r2 = rctau[:, 4][idx]

        return tau1, tau2, r0, r1, r2

    def v_ecm(self, soc, ocv, rctau):
        """
        Determine voltage from equivalent circuit model.
        """
        dt = np.diff(self.data.time)    # length of each time step, dt is not constant
        nc = len(self.data.current)     # total number of time steps based on current
        v0 = np.zeros(nc)               # initialize v0 array
        v1 = np.zeros(nc)               # initialize v1 array
        v2 = np.zeros(nc)               # initialize v2 array

        for k in range(1, nc):
            i = self.data.current[k]

            # get parameters at state of charge
            tau1, tau2, r0, r1, r2 = self.get_rtau(rctau, soc[k])

            # voltage in r0 resistor
            v0[k] = r0 * i

            # voltage in c1 capacitor
            tm1 = v1[k - 1] * np.exp(-dt[k - 1] / tau1)
            tm2 = r1 * (1 - np.exp(-dt[k - 1] / tau1)) * i
            v1[k] = tm1 + tm2

            # voltage in c2 capacitor
            tm3 = v2[k - 1] * np.exp(-dt[k - 1] / tau2)
            tm4 = r2 * (1 - np.exp(-dt[k - 1] / tau2)) * i
            v2[k] = tm3 + tm4

        vecm = ocv + v0 + v1 + v2
        return vecm

    def therm(self, ocv, proc, vecm):
        """
        Determine temperature profile from discharge data.
        """
        curr = self.data.current
        time = self.data.time

        asurf = self.params.a_surf
        cp = self.params.cp
        hconv = self.params.h_conv
        mcell = self.params.m_cell

        dt = np.diff(time)  # length of each time step
        nc = len(curr)      # total number of time steps based on current

        temp = np.zeros(nc)
        temp[0] = proc.tc4[0] + 273.15
        tinf = self.params.tinf

        for k in range(1, nc):
            i = curr[k]
            q_ecm = (vecm[k] - ocv[k]) * i
            q_conv = hconv * asurf * (temp[k] - tinf)
            q = q_ecm - q_conv
            dT = (q / (mcell * cp)) * dt[k]
            temp[k + 1] = dT + temp[k]

        return temp
