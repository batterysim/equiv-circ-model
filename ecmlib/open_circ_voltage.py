import numpy as np


def ocv(v_pts, z_pts, soc):
    """
    Linearly interpolate the open circuit voltage (OCV) from state of charge
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

    ocv = np.interp(soc, z_pts[::-1], v_pts[::-1])

    return ocv
