import matplotlib.pyplot as plt
from .utils import config_ax


def plot_module_hppc(data):
    """
    Plot battery module HPPC data.
    """

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, color='C3')
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))
