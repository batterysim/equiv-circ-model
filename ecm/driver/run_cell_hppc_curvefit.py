import params
import plotter
import printer

from cell_hppc_data import CellHppcData
from equiv_circ_model import EquivCircModel


def run_cell_hppc_curvefit():
    """
    here
    """

    file = params.datafiles['cell_hppc']
    data = CellHppcData.process(file)
    ecm = EquivCircModel(data, params)

    printer.print_parameters(params)
    printer.print_coeffs(ecm)
    plotter.plot_curvefit(data, ecm)
    plotter.show_plots()
