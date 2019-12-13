import params
import plotter

from hppc_data import HppcData


def view_hppc_data():
    """
    View plots of the HPPC data.
    """

    file = params.datafiles['hppc']
    data_orig = HppcData(file)
    data_proc = HppcData.process(file)

    plotter.plot_hppc_orig(data_orig)
    plotter.plot_hppc_proc(data_proc)
    plotter.show_plots()
