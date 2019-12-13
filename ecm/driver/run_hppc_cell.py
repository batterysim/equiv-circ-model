import params
import plotter

from hppc_data import HppcData
from equiv_circ_model import EquivCircModel


def run_hppc_cell():
    """
    """

    file = params.datafiles['hppc']
    data = HppcData.process(file)

    ecm = EquivCircModel(data, params)
    soc = ecm.soc()
    ocv = ecm.ocv(soc)
    coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs)
    vt = ecm.vt(soc, ocv, rctau)

    plotter.plot_vt(data, vt)
    plotter.show_plots()
