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

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_all.time, data_all.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_hppc.time, data_hppc.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

plt.show()
