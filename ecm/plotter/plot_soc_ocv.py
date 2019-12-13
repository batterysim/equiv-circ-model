import matplotlib.pyplot as plt

from .utils import config_ax


def plot_soc_ocv(data, ocv, soc, i_pts, t_pts, v_pts, z_pts):
    """
    Plot SOC and OCV from equivalent circuit model.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3', label='data')
    ax.plot(t_pts, v_pts, 'x', label='ocv pts')
    ax.plot(data.time, ocv, '--', label='ocv')
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

    fig, ax1 = plt.subplots(tight_layout=True)
    ax1.plot(data.time, data.current, 'C9', label='data')
    ax1.plot(t_pts, i_pts, 'x', label='ocv pts')
    ax1.legend(loc='lower left')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Current [A]', color='C0')
    ax1.tick_params('y', colors='C0')
    ax1.set_frame_on(False)
    ax2 = ax1.twinx()
    ax2.plot(data.time, soc, 'm', label='soc')
    ax2.plot(t_pts, z_pts, 'xC6', label='soc pts')
    ax2.legend(loc='best')
    ax2.set_ylabel('SOC [-]', color='m')
    ax2.tick_params('y', colors='m')
    ax2.set_frame_on(False)

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(z_pts, v_pts, 'm', marker='x')
    config_ax(ax, xylabels=('State of charge [-]', 'Open circuit voltage [V]'))
