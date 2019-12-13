import matplotlib.pyplot as plt
from .utils import config_ax


def plot_curvefit(data, ecm):
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
        config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), title=f'SOC section {i}', loc='best')

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(data.time, data.voltage, 'C3', label='data')
    ax.plot(data.time[id2], data.voltage[id2], 'x', label='id2')
    ax.plot(data.time[id4], data.voltage[id4], 'x', label='id4')
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')
