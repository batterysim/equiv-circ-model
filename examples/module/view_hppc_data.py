"""
View plots of the HPPC battery module data.
"""

import matplotlib.pyplot as plt

from ecm import ModuleHppcData
from ecm import config_ax

# Data from HPPC battery module test
# ----------------------------------------------------------------------------

file = '../data/module1-electchar-65ah-23deg.csv'
data_all = ModuleHppcData(file, all_data=True)
data_hppc = ModuleHppcData(file)

ids = data_hppc.get_indices_s()
idd = data_hppc.get_indices_discharge()

# Plot all data from HPPC battery module test
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_all.time, data_all.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_all.time, data_all.current)
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

# Plot section of HPPC data from HPPC battery module test
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.current)
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.voltage, color='C3')
ax.plot(data_hppc.time[ids], data_hppc.voltage[ids], 'x', label='ids')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.voltage, color='C3')
ax.plot(data_hppc.time[ids], data_hppc.voltage[ids], 'x', label='ids')
ax.plot(data_hppc.time[idd[0]], data_hppc.voltage[idd[0]], 'o', alpha=0.8, mew=0, label='idd0')
ax.plot(data_hppc.time[idd[1]], data_hppc.voltage[idd[1]], 'o', alpha=0.8, mew=0, label='idd1')
ax.plot(data_hppc.time[idd[2]], data_hppc.voltage[idd[2]], 'o', alpha=0.8, mew=0, label='idd2')
ax.plot(data_hppc.time[idd[3]], data_hppc.voltage[idd[3]], 'o', alpha=0.8, mew=0, label='idd3')
ax.plot(data_hppc.time[idd[4]], data_hppc.voltage[idd[4]], 'o', alpha=0.8, mew=0, label='idd4')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

plt.show()
