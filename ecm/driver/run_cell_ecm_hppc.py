import params
import plotter

from cell_hppc_data import CellHppcData
from equiv_circ_model import EquivCircModel


def run_cell_ecm_hppc():
    """
    """

    file = params.datafiles['cell_hppc']
    data = CellHppcData.process(file)

    ecm = EquivCircModel(data, params)
    soc = ecm.soc()
    ocv = ecm.ocv(soc)
    coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs)
    vt = ecm.vt(soc, ocv, rctau)

    plotter.plot_vt(data, vt)
    plotter.show_plots()
