import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def _config(ax, xlabel, ylabel, title=None, loc=None):
    """
    Configure labels and appearance of the plot figure.
    """
    ax.grid(True, color='0.9')
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')
    if title is not None:
        ax.set_title(title)
    if loc is not None:
        ax.legend(loc=loc)


def plot_hppc_orig(data):
    """
    Plot original HPPC data from battery cell test.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.current, 'C0')
    _config(ax, 'Time [s]', 'Current [A]')

    fig, ax = plt.subplots()
    ax.plot(data.time, data.voltage, 'C3')
    ax.arrow(15474, 4.06, 0, -0.14, head_width=1000, head_length=0.05, zorder=20)
    _config(ax, 'Time [s]', 'Voltage [V]')
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
    _config(ax, 'Time [s]', 'Current [A]', loc='best')

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3')
    ax.plot(data.time[ids], data.voltage[ids], 'x', label='ids')
    ax.plot(data.time[idq], data.voltage[idq], 'x', label='idq')
    ax.plot(data.time[idrc[0]], data.voltage[idrc[0]], 'o', alpha=0.8, mew=0, label='id0')
    ax.plot(data.time[idrc[1]], data.voltage[idrc[1]], 'o', alpha=0.8, mew=0, label='id1')
    ax.plot(data.time[idrc[2]], data.voltage[idrc[2]], 'o', alpha=0.8, mew=0, label='id2')
    ax.plot(data.time[idrc[3]], data.voltage[idrc[3]], 'o', alpha=0.8, mew=0, label='id3')
    ax.plot(data.time[idrc[4]], data.voltage[idrc[4]], 'o', alpha=0.8, mew=0, label='id4')
    _config(ax, 'Time [s]', 'Voltage [V]', loc='best')


def plot_discharge_orig(data):
    """
    Plot original discharge data from battery cell test.
    """
    ids = data.get_ids()
    id0, id1, id2, id3 = data.get_idx()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), tight_layout=True)
    ax1.plot(data.time, data.current, 'C0', label='data')
    ax1.plot(data.time[ids], data.current[ids], 'x', label='ids')
    ax1.plot(data.time[id0], data.current[id0], 'o', alpha=0.8, mew=0, label='id0')
    ax1.plot(data.time[id1], data.current[id1], 'o', alpha=0.8, mew=0, label='id1')
    ax1.plot(data.time[id2], data.current[id2], 'o', alpha=0.8, mew=0, label='id2')
    ax1.plot(data.time[id3], data.current[id3], 'o', alpha=0.8, mew=0, label='id3')
    ax2.plot(data.time, data.voltage, 'C3', label='data')
    ax2.plot(data.time[ids], data.voltage[ids], 'x', label='ids')
    ax2.plot(data.time[id0], data.voltage[id0], 'o', alpha=0.8, mew=0, label='id0')
    ax2.plot(data.time[id1], data.voltage[id1], 'o', alpha=0.8, mew=0, label='id1')
    ax2.plot(data.time[id2], data.voltage[id2], 'o', alpha=0.8, mew=0, label='id2')
    ax2.plot(data.time[id3], data.voltage[id3], 'o', alpha=0.8, mew=0, label='id3')
    _config(ax1, 'Time [s]', 'Current [A]', loc='best')
    _config(ax2, 'Time [s]', 'Voltage [V]', loc='best')

    fig, ax1 = plt.subplots(tight_layout=True)
    ax1.plot(data.time, data.current, 'C0')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Current [A]', color='C0')
    ax1.tick_params('y', colors='C0')
    ax1.set_frame_on(False)
    ax2 = ax1.twinx()
    ax2.plot(data.time, data.voltage, 'C3')
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Voltage [V]', color='C3')
    ax2.tick_params('y', colors='C3')
    ax2.set_frame_on(False)


def plot_discharge_proc(data):
    """
    Plot processed discharge data from battery cell test.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), tight_layout=True)
    ax1.plot(data.time, data.current, 'C0')
    ax2.plot(data.time, data.voltage, 'C3')
    _config(ax1, 'Time [s]', 'Current [A]')
    _config(ax2, 'Time [s]', 'Voltage [V]')


def plot_temp_orig(data):
    """
    Plot original temperature data from battery cell test.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.tc1, label='tc1')
    ax.plot(data.time, data.tc2, label='tc2')
    ax.plot(data.time, data.tc3, label='tc3')
    ax.plot(data.time, data.tc4, label='tc4')
    ax.axvspan(data.time[data.id0], data.time[data.id1], facecolor='0.9', label='section')
    _config(ax, 'Time [s]', 'Temperature [°C]', loc='best')


def plot_temp_proc(data):
    """
    Plot processed temperature data from battery cell test.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.tc1, label='tc1')
    ax.plot(data.time, data.tc2, label='tc2')
    ax.plot(data.time, data.tc3, label='tc3')
    ax.plot(data.time, data.tc4, label='tc4')
    _config(ax, 'Time [s]', 'Temperature [°C]', loc='best')


def plot_soc_ocv(data, ocv, soc, i_pts, t_pts, v_pts, z_pts):
    """
    Plot SOC and OCV from equivalent circuit model.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3', label='data')
    ax.plot(t_pts, v_pts, 'x', label='ocv pts')
    ax.plot(data.time, ocv, '--', label='ocv')
    _config(ax, 'Time [s]', 'Voltage [V]', loc='best')

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
    ax2.set_ylabel('SOC [-]', color='C6')
    ax2.tick_params('y', colors='C6')
    ax2.set_frame_on(False)

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(z_pts, v_pts, 'm', marker='x')
    _config(ax, 'State of charge [-]', 'Open circuit voltage [V]')


def plot_curve_fit(data, ecm):
    """
    Plot curve fit for one time constant (OTC) and two time constant (TTC)
    functions. Plots are generated for each SOC section in HPPC profile.
    """
    coeffs_otc = ecm.curve_fit_coeff(ecm.func_otc, 3)
    coeffs_ttc = ecm.curve_fit_coeff(ecm.func_ttc, 5)

    # indices representing start (id2) and end (id4) of curve in each SOC section
    _, _, id2, _, id4 = data.get_idrc()

    for i in range(len(id2)):
        start = id2[i]
        end = id4[i]
        t_curve = data.time[start:end]
        v_curve = data.voltage[start:end]
        t_scale = t_curve - t_curve[0]

        vfit1 = ecm.func_otc(t_scale, *coeffs_otc[i])
        vfit2 = ecm.func_ttc(t_scale, *coeffs_ttc[i])

        fig, ax = plt.subplots()
        ax.plot(t_curve, v_curve, 'C3', marker='.', label='data')
        ax.plot(t_curve, vfit1, label='otc')
        ax.plot(t_curve, vfit2, label='ttc')
        _config(ax, 'Time [s]', 'Voltage [V]', title=f'SOC section {i}', loc='best')

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3', label='data')
    ax.plot(data.time[id2], data.voltage[id2], 'x', label='id2')
    ax.plot(data.time[id4], data.voltage[id4], 'x', label='id4')
    _config(ax, 'Time [s]', 'Voltage [V]', loc='best')


def plot_v_ecm(data, v_ecm):
    """
    Plot HPPC voltage data and ECM voltage. Plot absolute voltage difference
    between HPPC data and ECM.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3', label='data')
    ax.plot(data.time, v_ecm, 'k--', label='ecm')
    _config(ax, 'Time [s]', 'Voltage [V]', loc='best')

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, abs(data.voltage - v_ecm))
    _config(ax, 'Time [s]', 'Absolute voltage difference [V]')


def show_plots():
    """
    Show all plot figures.
    """
    plt.show()
