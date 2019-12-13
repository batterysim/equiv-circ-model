import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from .utils import config_ax


def plot_hppc_orig(data):
    """
    Plot original HPPC data from battery cell test.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.current, 'C0')
    config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

    fig, ax = plt.subplots()
    ax.plot(data.time, data.voltage, 'C3')
    ax.arrow(15474, 4.06, 0, -0.14, head_width=1000, head_length=0.05, zorder=20)
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))
    axins = inset_axes(ax, 2, 2, loc='lower left', borderpad=4)
    axins.plot(data.time, data.voltage, 'C3')
    axins.set_xlim(15420, 15540)
    axins.set_ylim(4.08, 4.21)
    plt.xticks(visible=False)
    plt.yticks(visible=False)

    fig, ax1 = plt.subplots(tight_layout=True)
    ax1.plot(data.time, data.current, 'C0')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Current [A]', color='C0')
    ax1.tick_params('y', colors='C0')
    ax1.set_frame_on(False)
    ax2 = ax1.twinx()
    ax2.plot(data.time, data.voltage, 'C3')
    ax2.set_ylabel('Voltage [V]', color='C3')
    ax2.tick_params('y', colors='C3')
    ax2.set_frame_on(False)


def plot_hppc_proc(data):
    """
    Plot processed HPPC data from battery cell test.
    """
    ids = data.get_ids()
    idq = data.get_idq()
    idrc = data.get_idrc()

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.current, 'C0')
    ax.plot(data.time[ids], data.current[ids], 'x', label='ids')
    ax.plot(data.time[idq], data.current[idq], 'x', label='idq')
    config_ax(ax, xylabels=('Time [s]', 'Current [A]'), loc='best')

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3')
    ax.plot(data.time[ids], data.voltage[ids], 'x', label='ids')
    ax.plot(data.time[idq], data.voltage[idq], 'x', label='idq')
    ax.plot(data.time[idrc[0]], data.voltage[idrc[0]], 'o', alpha=0.8, mew=0, label='id0')
    ax.plot(data.time[idrc[1]], data.voltage[idrc[1]], 'o', alpha=0.8, mew=0, label='id1')
    ax.plot(data.time[idrc[2]], data.voltage[idrc[2]], 'o', alpha=0.8, mew=0, label='id2')
    ax.plot(data.time[idrc[3]], data.voltage[idrc[3]], 'o', alpha=0.8, mew=0, label='id3')
    ax.plot(data.time[idrc[4]], data.voltage[idrc[4]], 'o', alpha=0.8, mew=0, label='id4')
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')
