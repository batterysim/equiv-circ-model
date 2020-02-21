"""
View plots of the HPPC battery cell data.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from ecm import CellHppcData
from ecm import config_ax

# Data from HPPC battery cell test
# ----------------------------------------------------------------------------

file = '../data/cell-low-current-hppc-25c-2.csv'

data_all = CellHppcData(file, all_data=True)
ids_all = data_all.get_indices_s()

data_hppc = CellHppcData(file)
ids = data_hppc.get_indices_s()
idq = data_hppc.get_indices_q()
idp = data_hppc.get_indices_pulse()
idd = data_hppc.get_indices_discharge()

# Plot all data from HPPC battery cell test
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_all.time, data_all.voltage, 'C3', label='data')
ax.plot(data_all.time[ids_all], data_all.voltage[ids_all], 'x', label='ids all')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_all.time, data_all.current, 'C0')
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

fig, ax = plt.subplots()
ax.plot(data_all.time, data_all.voltage, 'C3')
ax.arrow(15474, 4.06, 0, -0.14, head_width=1000, head_length=0.05, zorder=20)
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))
axins = inset_axes(ax, 2, 2, loc='lower left', borderpad=4)
axins.plot(data_all.time, data_all.voltage, 'C3')
axins.set_xlim(15420, 15540)
axins.set_ylim(4.08, 4.21)
plt.xticks(visible=False)
plt.yticks(visible=False)

fig, ax1 = plt.subplots(tight_layout=True)
ax1.plot(data_all.time, data_all.current, 'C0')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Current [A]', color='C0')
ax1.tick_params('y', colors='C0')
ax1.set_frame_on(False)
ax2 = ax1.twinx()
ax2.plot(data_all.time, data_all.voltage, 'C3')
ax2.set_ylabel('Voltage [V]', color='C3')
ax2.tick_params('y', colors='C3')
ax2.set_frame_on(False)

# Plot section of HPPC data from HPPC battery cell test
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.current, 'C0')
ax.plot(data_hppc.time[ids], data_hppc.current[ids], 'x', label='ids')
ax.plot(data_hppc.time[idq], data_hppc.current[idq], 'x', label='idq')
config_ax(ax, xylabels=('Time [s]', 'Current [A]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.voltage, 'C3')
ax.plot(data_hppc.time[ids], data_hppc.voltage[ids], 'x', label='ids')
ax.plot(data_hppc.time[idq], data_hppc.voltage[idq], 'x', label='idq')
ax.plot(data_hppc.time[idp[0]], data_hppc.voltage[idp[0]], 'o', alpha=0.8, mew=0, label='idp0')
ax.plot(data_hppc.time[idp[1]], data_hppc.voltage[idp[1]], 'o', alpha=0.8, mew=0, label='idp1')
ax.plot(data_hppc.time[idp[2]], data_hppc.voltage[idp[2]], 'o', alpha=0.8, mew=0, label='idp2')
ax.plot(data_hppc.time[idp[3]], data_hppc.voltage[idp[3]], 'o', alpha=0.8, mew=0, label='idp3')
ax.plot(data_hppc.time[idp[4]], data_hppc.voltage[idp[4]], 'o', alpha=0.8, mew=0, label='idp4')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.voltage, 'C3')
ax.plot(data_hppc.time[ids], data_hppc.voltage[ids], 'x', label='ids')
ax.plot(data_hppc.time[idq], data_hppc.voltage[idq], 'x', label='idq')
ax.plot(data_hppc.time[idd[0]], data_hppc.voltage[idd[0]], 'o', alpha=0.8, mew=0, label='idd0')
ax.plot(data_hppc.time[idd[1]], data_hppc.voltage[idd[1]], 'o', alpha=0.8, mew=0, label='idd1')
ax.plot(data_hppc.time[idd[2]], data_hppc.voltage[idd[2]], 'o', alpha=0.8, mew=0, label='idd2')
ax.plot(data_hppc.time[idd[3]], data_hppc.voltage[idd[3]], 'o', alpha=0.8, mew=0, label='idd3')
ax.plot(data_hppc.time[idd[4]], data_hppc.voltage[idd[4]], 'o', alpha=0.8, mew=0, label='idd4')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

plt.show()
