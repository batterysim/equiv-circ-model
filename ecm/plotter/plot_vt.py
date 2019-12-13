import matplotlib.pyplot as plt
from .utils import config_ax


def plot_vt(data, vt):
    """
    Plot HPPC voltage data and ECM voltage. Plot absolute voltage difference
    between HPPC data and ECM.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3', label='data')
    ax.plot(data.time, vt, 'k--', label='ecm')
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, abs(data.voltage - vt))
    config_ax(ax, xylabels=('Time [s]', 'Absolute voltage difference [V]'))
