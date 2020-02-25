"""
Helper functions to calculate vt from cell ECM and module ECM to predict
battery pack voltage. Helper function to calculate
"""

import numpy as np


def get_vt_cell_pack(params, n_parallel, data_us06, ecm):

    # RC parameters for cell ECM
    soc = ecm.soc()
    _, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)
    coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs)

    # Cell ECM to pack calculations
    ecm.current = data_us06.current / n_parallel
    ecm.time = data_us06.time
    ecm.q_cell = params.q_module / n_parallel

    soc = ecm.soc()
    ocv = ecm.ocv(soc, vz_pts=(v_pts, z_pts))
    vt = ecm.vt(soc, ocv, rctau)
    vt_pack = vt * 5.965

    return vt_pack


def get_vt_module_pack(data_us06, ecm):

    # RC parameters for module ECM
    soc = ecm.soc()
    _, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)
    coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs)

    # Module ECM to pack calculations
    ecm.current = data_us06.current
    ecm.time = data_us06.time

    soc = ecm.soc()
    ocv = ecm.ocv(soc, vz_pts=(v_pts, z_pts))
    vt = ecm.vt(soc, ocv, rctau)
    vt_pack = vt * 2.985

    return vt_pack


def r2fit(y, y_fit):

    # residual sum of squares
    ss_res = np.sum((y - y_fit) ** 2)

    # total sum of squares
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    # r-squared
    r2 = 1 - (ss_res / ss_tot)

    return r2
