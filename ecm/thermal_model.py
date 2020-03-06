import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp


class ThermalModel:
    """
    Thermal model for battery cell temperature.

    Parameters
    ----------
    params : module
        Parameters needed for the thermal calculations. The parameters module
        must contain variables for `tinf`, `m_cell`, `h_conv`, `cp_cell`, and
        `a_surf`.

    Attributes
    ----------
    tf : float
        Ambient temperature [K]
    m : float
        Mass of the battery cell or battery module [kg]
    h : float
        Convective heat transfer coefficient W/(m² K)]
    cp : float
        Heat capacity of the battery cell or battery module [J/(kg K)]
    sa : float
        Surface area of the battery cell [m²]

    Methods
    -------
    calc_q(i, ocv, vt)
        Calculate heat generation of battery cell.
    calc_q_temp(i, ocv, time, ti, vt)
        Calculate heat generation and temperature of battery cell.
    """

    def __init__(self, params):
        """
        Initialize with module containing parameters for the battery cell or
        battery module.
        """
        # self.rc = params.rc
        # self.ru = params.ru
        # self.cc = params.cc
        # self.cs = params.cs

        self.tf = params.tinf
        self.m = params.m_cell
        self.h = params.h_conv
        self.cp = params.cp_cell
        self.sa = params.a_surf

    def solve_tc_ts(self, q, time):
        """
        """
        rc = self.rc
        ru = self.ru
        cc = self.cc
        cs = self.cs
        tf = self.tf

        interp_qt = interp1d(time, q)

        def tc_dt(t, tc, ts, q):
            """
            dTc/dt = (Ts-Tc)/(Rc*Cc) + Q/Cc
            """
            return ((ts - tc) / (rc * cc)) + q / cc

        def ts_dt(t, tc, ts):
            """
            dTs/dt = (Tf-Ts)/(Ru*Cs) - (Ts-Tc)/(Rc*Cs)
            """
            return ((tf - ts) / (ru * cs)) - ((ts - tc) / (rc * cs))

        def jacobian(t, y):
            """
            Given the following system of ODEs

                dTc/dt = (Ts-Tc)/(Rc*Cc) + Q/Cc
                dTs/dt = (Tf-Ts)/(Ru*Cs) - (Ts-Tc)/(Rc*Cs)

            determine the Jacobian matrix of the right-hand side as

                Jacobian matrix = [df1/dTc, df2/dTc]
                                  [df1/dTs, df2/dTs]

                f1 = (Ts-Tc)/(Rc*Cc) + Q/Cc
                f2 = (Tf-Ts)/(Ru*Cs) - (Ts-Tc)/(Rc*Cs)

            The partial derivatives of the Jacobian were calculated with SymPy.
            """
            cc = 62.7
            cs = 4.5
            rc = 1.94
            ru = 3.08
            jc = np.array([
                [-1 / (cc * rc), 1 / (cs * rc)],
                [1 / (cc * rc), -1 / (cs * ru) - 1 / (cs * rc)]
            ])
            return jc

        def func(t, y):
            """
            Right-hand side of the system of ODEs.
            """
            q = interp_qt(t)
            tcdt = tc_dt(t, y[0], y[1], q)
            tsdt = ts_dt(t, y[0], y[1])
            return tcdt, tsdt

        tspan = (time[0], time[-1])
        sol = solve_ivp(func, tspan, (298.15, 298.15), method='BDF', t_eval=time, jac=jacobian)

        tc = sol.y[0]
        ts = sol.y[1]
        return tc, ts

    def calc_q(self, *, i, ocv, vt):
        """
        Calculate heat generation as difference between terminal voltage and
        open circuit voltage.

        Parameters
        ----------
        i : array
            Current applied to battery cell [A]
        ocv : array
            Open circuit voltage of the battery cell [V]
        vt : array
            Terminal voltage of the battery cell [V]

        Returns
        -------
        q_gen : array
            Heat generation from battery cell [W]
        """
        nt = len(vt)
        q_gen = np.zeros(nt)

        for n in range(nt - 1):
            q_irrev = i[n] * (vt[n] - ocv[n])
            q = q_irrev
            q_gen[n + 1] = q

        return q_gen

    def calc_q_temp(self, *, i, ocv, time, ti, vt):
        """
        Calculate heat generation and temperature of the battery cell.

        Parameters
        ----------
        i : array
            Current applied to battery cell [A]
        ocv : array
            Open circuit voltage of the battery cell [V]
        time : array
            Time associated with data points [s]
        ti : float
            Initial temperature of the battery cell [K]
        vt : array
            Terminal voltage of the battery cell [V]

        Returns
        -------
        q_gen : array
            Heat generation from battery cell [W]
        tk : array
            Temperature of the battery cell [K]
        """
        dt = np.diff(time)
        nt = len(vt)

        q_gen = np.zeros(nt)
        tk = np.zeros(nt)
        tk[0] = ti

        for n in range(nt - 1):
            q_irrev = i[n] * (vt[n] - ocv[n])
            q_conv = self.h * self.sa * (self.tf - tk[n])
            q = q_irrev + q_conv
            q_gen[n + 1] = q
            tk[n + 1] = tk[n] + (q / (self.m * self.cp)) * dt[n]

        return q_gen, tk
