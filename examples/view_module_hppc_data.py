"""
View plots of the battery module HPPC data.
"""

import matplotlib.pyplot as plt

from ecm import ModuleHppcData
from utils import config_ax

# Data from HPPC battery module test
# ----------------------------------------------------------------------------

file = 'data/module1-electchar-65ah-45deg.csv'
data_all = ModuleHppcData(file, all_data=True)
data_hppc = ModuleHppcData(file)

ids = data_hppc.get_ids()
idx = data_hppc.get_idx()

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
ax.plot(data_hppc.time, data_hppc.voltage, color='C3')
ax.plot(data_hppc.time[ids], data_hppc.voltage[ids], 'x', label='ids')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.voltage, color='C3')
ax.plot(data_hppc.time[idx[0]], data_hppc.voltage[idx[0]], 'o', mew=0, label='idx0')
ax.plot(data_hppc.time[idx[1]], data_hppc.voltage[idx[1]], 'o', mew=0, label='idx1')
ax.plot(data_hppc.time[idx[2]], data_hppc.voltage[idx[2]], 'o', mew=0, label='idx2')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.current)
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

plt.show()
