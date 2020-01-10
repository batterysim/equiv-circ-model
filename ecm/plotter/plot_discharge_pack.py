import matplotlib.pyplot as plt
from .utils import config_ax


def plot_discharge_pack(time, current, voltage, vt_dis, n_cells, i_cells2, v_cells, temp_cells):
    """
    Plot battery pack model results for constant current discharge.

    Parameters
    ----------
    time : ndarray
        Time from discharge data [s]
    current : ndarray
        Current from discharge data [A]
    voltage : ndarray
        Voltage from discharge data [V]
    vt_dis : ndarray
        Discharge voltage from equivalent circuit model for a single battery cell [V]
    n_cells : int
        Total number of cells in battery pack [-]
    i_cells2 : ndarray
        Branch current for each battery cell [A]
    v_cells : ndarray
        Discharge voltage from equivalent circuit model for each cell in battery pack [V]
    temp_cells : ndarray
        Temperature from thermal model for each cell in battery pack [K]
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(time, current, marker='.')
    config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(time, voltage, marker='.')
    ax.plot(time, vt_dis)
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

    fig, ax = plt.subplots(tight_layout=True)
    for k in range(n_cells):
        ax.plot(time, i_cells2[k], label=f'cell {k+1}')
    config_ax(ax, xylabels=('Time [s]', 'Current [A]'), loc='best')

    fig, ax = plt.subplots(tight_layout=True)
    for k in range(n_cells):
        ax.plot(time, v_cells[k], label=f'cell {k+1}')
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

    fig, ax = plt.subplots(tight_layout=True)
    for k in range(n_cells):
        ax.plot(time, temp_cells[k], label=f'cell {k+1}')
    config_ax(ax, xylabels=('Time [s]', 'Temperature [K]'), loc='best')
