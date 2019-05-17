import numpy as np


def soc(current, time, eta_chg, eta_dis, q_cell):
    """
    State of charge (SOC) of a battery cell based on the method from
    Gregory Plett's book [#plett]. Fully charged is SOC=1 and fully
    discharged is SOC=0. SOC is also referred to as `z` in some texts.

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

    q = q_cell * 3600
    dt = np.diff(time)

    nc = len(current)
    z = np.ones(nc)

    for k in range(1, nc):
        i = current[k]
        if i > 0:
            eta = eta_chg
        else:
            eta = eta_dis
        z[k] = z[k - 1] + ((eta * i * dt[k - 1]) / q)

    return z
