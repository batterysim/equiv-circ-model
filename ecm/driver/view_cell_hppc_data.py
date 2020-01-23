import params
import plotter

from cell_hppc_data import CellHppcData


def view_cell_hppc_data():
    """
    View plots of the battery cell HPPC data.
    """

    file = params.datafiles['hppc']
    data_orig = CellHppcData(file)
    data_proc = CellHppcData.process(file)

    plotter.plot_hppc_orig(data_orig)
    plotter.plot_hppc_proc(data_proc)
    plotter.show_plots()
