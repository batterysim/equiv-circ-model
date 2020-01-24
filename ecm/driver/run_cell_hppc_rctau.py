import params
import printer

from cell_hppc_data import CellHppcData
from equiv_circ_model import EquivCircModel


def run_cell_hppc_rctau():
    """
    """
    file = params.datafiles['cell_hppc']
    data = CellHppcData.process(file)

    ecm = EquivCircModel(data, params)
    coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs)

    printer.print_parameters(params)
    printer.print_rctau(rctau)
