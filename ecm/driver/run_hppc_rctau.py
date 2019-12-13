import params
import printer

from hppc_data import HppcData
from equiv_circ_model import EquivCircModel


def run_hppc_rctau():
    """
    """
    file = params.datafiles['hppc']
    data = HppcData.process(file)

    ecm = EquivCircModel(data, params)
    coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs)

    printer.print_parameters(params)
    printer.print_rctau(rctau)
