import params
import plotter
from module_data import ModuleData


def view_module_hppc_data():
    """
    View plots of the battery module HPPC data.
    """

    file = params.datafiles['module1_hppc_45deg']
    data = ModuleData(file)

    plotter.plot_module_hppc(data)
    plotter.show_plots()
