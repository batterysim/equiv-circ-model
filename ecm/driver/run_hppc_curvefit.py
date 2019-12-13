import params
import plotter
import printer

from hppc_data import HppcData
from equiv_circ_model import EquivCircModel


def run_hppc_curvefit():
    """
    here
    """

    file = params.datafiles['hppc']
    data = HppcData.process(file)
    ecm = EquivCircModel(data, params)

    printer.print_parameters(params)
    printer.print_coeffs(ecm)
    plotter.plot_curvefit(data, ecm)
    plotter.show_plots()
