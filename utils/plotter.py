import matplotlib.pyplot as plt


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


def plot_data(data):
    """
    Plot battery data from battery cell test.
    """
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3')
    _config(ax, 'Time [s]', 'Voltage [V]')

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.current, 'C9')
    _config(ax, 'Time [s]', 'Current [A]')

    plt.show()


def plot_soc_ocv(data, ecm):
    """
    Plot SOC and OCV from equivalent circuit model.
    """
    i_pts, t_pts, v_pts, soc_pts = ecm.points

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3', label='data')
    ax.plot(t_pts, v_pts, 'x', label='ocv pts')
    ax.plot(data.time, ecm.ocv, '--', label='ocv')
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
    ax2.plot(data.time, ecm.soc, 'm', label='soc')
    ax2.plot(t_pts, soc_pts, 'xC6', label='soc pts')
    ax2.legend(loc='best')
    ax2.set_ylabel('SOC [-]', color='C6')
    ax2.tick_params('y', colors='C6')
    ax2.set_frame_on(False)

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(soc_pts, v_pts, 'm', marker='x')
    _config(ax, 'State of charge [-]', 'Open circuit voltage [V]')

    plt.show()


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

    plt.show()


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

    plt.show()
