import params
import plotter
import printer

from hppc_data import HppcData
from equiv_circ_model import EquivCircModel


def run_hppc_sococv():
    """
    """
    file = params.datafiles['hppc']
    data = HppcData.process(file)

    ecm = EquivCircModel(data, params)
    soc = ecm.soc()
    ocv, i_pts, t_pts, v_pts, z_pts = ecm.ocv(soc, pts=True)

    printer.print_parameters(params)
    printer.print_soc_ocv(v_pts, z_pts)

    plotter.plot_soc_ocv(data, ocv, soc, i_pts, t_pts, v_pts, z_pts)
    plotter.show_plots()
