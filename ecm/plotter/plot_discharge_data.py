import matplotlib.pyplot as plt
from .utils import config_ax


def plot_orig_dis_electric_data(dis_1c, dis_2c, dis_3c):
    """
    Plot the original current and voltage discharge data.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 4.8), sharey=True, tight_layout=True)
    ax1.plot(dis_1c.time, dis_1c.current)
    ax2.plot(dis_2c.time, dis_2c.current)
    ax3.plot(dis_3c.time, dis_3c.current)
    config_ax(ax1, xylabels=('', 'Current [A]'))
    config_ax(ax2, xylabels=('Time [s]', ''))
    config_ax(ax3)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 4.8), sharey=True, tight_layout=True)
    ax1.plot(dis_1c.time, dis_1c.voltage, 'C3')
    ax2.plot(dis_2c.time, dis_2c.voltage, 'C3')
    ax3.plot(dis_3c.time, dis_3c.voltage, 'C3')
    config_ax(ax1, xylabels=('', 'Voltage [V]'))
    config_ax(ax2, xylabels=('Time [s]', ''))
    config_ax(ax3)


def plot_orig_dis_temps_data(temp_1c, temp_2c, temp_3c):
    """
    Plot the original temperatures from discharge data.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 4.8), sharey=True, tight_layout=True)
    ax1.plot(temp_1c.time, temp_1c.tc1)
    ax1.plot(temp_1c.time, temp_1c.tc2)
    ax1.plot(temp_1c.time, temp_1c.tc3)
    ax1.plot(temp_1c.time, temp_1c.tc4)
    ax2.plot(temp_2c.time, temp_2c.tc1)
    ax2.plot(temp_2c.time, temp_2c.tc2)
    ax2.plot(temp_2c.time, temp_2c.tc3)
    ax2.plot(temp_2c.time, temp_2c.tc4)
    ax3.plot(temp_3c.time, temp_3c.tc1, label='tc1')
    ax3.plot(temp_3c.time, temp_3c.tc2, label='tc2')
    ax3.plot(temp_3c.time, temp_3c.tc3, label='tc3')
    ax3.plot(temp_3c.time, temp_3c.tc4, label='tc4')
    config_ax(ax1, xylabels=('', 'Temperature [°C]'))
    config_ax(ax2, xylabels=('Time [s]', ''))
    config_ax(ax3, loc='upper right')


def plot_dis_electric_data(dis_1c, dis_2c, dis_3c, dis_only_1c, dis_only_2c, dis_only_3c):
    """
    Plot current and voltage from discharge data.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
    ax1.plot(dis_1c.time, dis_1c.current, marker='.', label='1c')
    ax1.plot(dis_2c.time, dis_2c.current, marker='.', label='2c')
    ax1.plot(dis_3c.time, dis_3c.current, marker='.', label='3c')
    config_ax(ax1, xylabels=('Time [s]', 'Current [A]'), loc='lower right')
    ax2.plot(dis_only_1c.time, dis_only_1c.current, marker='.', label='1c')
    ax2.plot(dis_only_2c.time, dis_only_2c.current, marker='.', label='2c')
    ax2.plot(dis_only_3c.time, dis_only_3c.current, marker='.', label='3c')
    config_ax(ax2, xylabels=('Time [s]', 'Current [A]'), loc='lower right')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
    ax1.plot(dis_1c.time, dis_1c.voltage, marker='.', label='1c')
    ax1.plot(dis_2c.time, dis_2c.voltage, marker='.', label='2c')
    ax1.plot(dis_3c.time, dis_3c.voltage, marker='.', label='3c')
    config_ax(ax1, xylabels=('Time [s]', 'Voltage [V]'), loc='upper right')
    ax2.plot(dis_only_1c.time, dis_only_1c.voltage, marker='.', label='1c')
    ax2.plot(dis_only_2c.time, dis_only_2c.voltage, marker='.', label='2c')
    ax2.plot(dis_only_3c.time, dis_only_3c.voltage, marker='.', label='3c')
    config_ax(ax2, xylabels=('Time [s]', 'Voltage [V]'), loc='upper right')


def plot_dis_temps_data(temp_1c, temp_2c, temp_3c, temp_only_1c, temp_only_2c, temp_only_3c):
    """
    Plot temperatures from discharge data.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
    ax1.plot(temp_1c.time, temp_1c.tc1, label='tc1')
    ax1.plot(temp_1c.time, temp_1c.tc2, label='tc2')
    ax1.plot(temp_1c.time, temp_1c.tc3, label='tc3')
    ax1.plot(temp_1c.time, temp_1c.tc4, label='tc4')
    ax1.plot(temp_1c.time, temp_1c.tavg, 'k', label='tavg')
    config_ax(ax1, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')
    ax2.plot(temp_only_1c.time, temp_only_1c.tc1, label='tc1')
    ax2.plot(temp_only_1c.time, temp_only_1c.tc2, label='tc2')
    ax2.plot(temp_only_1c.time, temp_only_1c.tc3, label='tc3')
    ax2.plot(temp_only_1c.time, temp_only_1c.tc4, label='tc4')
    ax2.plot(temp_only_1c.time, temp_only_1c.tavg, 'k', label='tavg')
    config_ax(ax2, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
    ax1.plot(temp_2c.time, temp_2c.tc1, label='tc1')
    ax1.plot(temp_2c.time, temp_2c.tc2, label='tc2')
    ax1.plot(temp_2c.time, temp_2c.tc3, label='tc3')
    ax1.plot(temp_2c.time, temp_2c.tc4, label='tc4')
    ax1.plot(temp_2c.time, temp_2c.tavg, 'k', label='tavg')
    config_ax(ax1, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')
    ax2.plot(temp_only_2c.time, temp_only_2c.tc1, label='tc1')
    ax2.plot(temp_only_2c.time, temp_only_2c.tc2, label='tc2')
    ax2.plot(temp_only_2c.time, temp_only_2c.tc3, label='tc3')
    ax2.plot(temp_only_2c.time, temp_only_2c.tc4, label='tc4')
    ax2.plot(temp_only_2c.time, temp_only_2c.tavg, 'k', label='tavg')
    config_ax(ax2, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
    ax1.plot(temp_3c.time, temp_3c.tc1, label='tc1')
    ax1.plot(temp_3c.time, temp_3c.tc2, label='tc2')
    ax1.plot(temp_3c.time, temp_3c.tc3, label='tc3')
    ax1.plot(temp_3c.time, temp_3c.tc4, label='tc4')
    ax1.plot(temp_3c.time, temp_3c.tavg, 'k', label='tavg')
    config_ax(ax1, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')
    ax2.plot(temp_only_3c.time, temp_only_3c.tc1, label='tc1')
    ax2.plot(temp_only_3c.time, temp_only_3c.tc2, label='tc2')
    ax2.plot(temp_only_3c.time, temp_only_3c.tc3, label='tc3')
    ax2.plot(temp_only_3c.time, temp_only_3c.tc4, label='tc4')
    ax2.plot(temp_only_3c.time, temp_only_3c.tavg, 'k', label='tavg')
    config_ax(ax2, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
    ax1.plot(temp_1c.time, temp_1c.tavg, marker='.', markevery=20, label='1c')
    ax1.plot(temp_2c.time, temp_2c.tavg, marker='.', markevery=20, label='2c')
    ax1.plot(temp_3c.time, temp_3c.tavg, marker='.', markevery=20, label='3c')
    ax1.fill_between(temp_1c.time, temp_1c.tmax, temp_1c.tmin, alpha=0.3)
    ax1.fill_between(temp_2c.time, temp_2c.tmax, temp_2c.tmin, alpha=0.3)
    ax1.fill_between(temp_3c.time, temp_3c.tmax, temp_3c.tmin, alpha=0.3)
    config_ax(ax1, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper right')
    ax2.plot(temp_only_1c.time, temp_only_1c.tavg, marker='.', markevery=20, label='1c')
    ax2.plot(temp_only_2c.time, temp_only_2c.tavg, marker='.', markevery=20, label='2c')
    ax2.plot(temp_only_3c.time, temp_only_3c.tavg, marker='.', markevery=20, label='3c')
    ax2.fill_between(temp_only_1c.time, temp_only_1c.tmax, temp_only_1c.tmin, alpha=0.3)
    ax2.fill_between(temp_only_2c.time, temp_only_2c.tmax, temp_only_2c.tmin, alpha=0.3)
    ax2.fill_between(temp_only_3c.time, temp_only_3c.tmax, temp_only_3c.tmin, alpha=0.3)
    config_ax(ax2, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper right')
