import numpy as np


def _get_rtau(rctau, z):
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


def v_ecm(curr, time, soc, ocv, rctau):
    """
    Determine voltage from equivalent circuit model.
    """

    dt = np.diff(time)      # length of each time step, dt is not constant
    nc = len(curr)          # total number of time steps based on current
    v0 = np.zeros(nc)       # initialize v0 array
    v1 = np.zeros(nc)       # initialize v1 array
    v2 = np.zeros(nc)       # initialize v2 array

    for k in range(1, nc):
        i = curr[k]

        # get parameters at state of charge
        tau1, tau2, r0, r1, r2 = _get_rtau(rctau, soc[k])

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
