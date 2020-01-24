"""
Battery pack where cells are connected in parallel to make a module. The
modules are connected in series to make a pack.

           |== Cell ==|       |== Cell ==|
i_pack  ---|== Cell ==|---*---|== Cell ==|---*
           |== Cell ==|       |== Cell ==|
"""

import numpy as np

import params
import plotter

from cell_discharge_data import CellDischargeData
from cell_hppc_data import CellHppcData
from equiv_circ_model import EquivCircModel
from thermal_model import ThermalModel


def run_pack_ecm_discharge():
    """
    """

    # Parameters
    # ----------------------------------------------------------------------------

    # number of cells in parallel to make a module
    n_parallel = 3

    # number of battery modules in series to make a pack
    n_series = 2

    # initial random state of charge (SOC) for each cell, zi units of [-]
    zi = np.random.uniform(0.95, 1.00, (n_series, n_parallel))

    # initial random capacity (Q) for each cell, qi units of [Ah]
    # qi = np.random.uniform(29, 30.7, (n_series, n_parallel))

    # total capacity [Ah] of battery pack
    # pack capacity is the minimum module capacity
    # q_pack = min(np.sum(qi, axis=1))

    # HPPC data
    # ----------------------------------------------------------------------------

    file_hppc = params.datafiles['cell_hppc']
    data_hppc = CellHppcData.process(file_hppc)

    ecm = EquivCircModel(data_hppc, params)
    soc = ecm.soc()
    _, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)

    coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs)

    # Discharge data
    # ----------------------------------------------------------------------------

    data_dis = CellDischargeData.process_discharge_only(params.datafiles['cell_discharge_1c'])

    ecm.current = data_dis.current
    ecm.voltage = data_dis.voltage
    ecm.time = data_dis.time

    soc_dis = ecm.soc()
    ocv_dis = ecm.ocv(soc_dis, vz_pts=(v_pts, z_pts))
    vt_dis = ecm.vt(soc_dis, ocv_dis, rctau)

    # Calculations for battery pack
    # ----------------------------------------------------------------------------

    ocv_cells = np.interp(zi, z_pts[::-1], v_pts[::-1])
    r0_cells = rctau[:, 2].mean() * np.ones((n_series, n_parallel))

    # current [A] applied to battery pack at 3C discharge rate
    i_pack = ecm.current * 3

    i_cells = np.zeros((len(i_pack), n_series, n_parallel))

    for k in range(1, len(i_pack)):
        v_modules = (np.sum(ocv_cells / r0_cells, axis=1) - i_pack[k]) / np.sum(1 / r0_cells, axis=1)
        i_cells[k] = ((ocv_cells.T - v_modules).T) / r0_cells

    i_cells2 = i_cells.transpose(1, 2, 0).reshape(i_cells[0].size, len(i_pack))

    n_cells = n_parallel * n_series
    v_cells = np.zeros((n_cells, len(i_pack)))
    temp_cells = np.zeros((n_cells, len(i_pack)))

    tm = ThermalModel(params)

    for k in range(n_cells):
        ecm.current = i_cells2[k]
        soc = ecm.soc()
        ocv = ecm.ocv(soc, vz_pts=(v_pts, z_pts))
        vt = ecm.vt(soc, ocv, rctau)
        v_cells[k] = vt

        icell = i_cells2[k]
        _, temp_cell = tm.calc_q_temp(i=icell, ocv=ocv, time=data_dis.time, ti=297, vt=vt)
        temp_cells[k] = temp_cell

    # Plot
    # ----------------------------------------------------------------------------

    plotter.plot_discharge_pack(
        data_dis.time, data_dis.current, data_dis.voltage, vt_dis, n_cells,
        i_cells2, v_cells, temp_cells
    )

    plotter.show_plots()
