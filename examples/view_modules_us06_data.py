"""
View plots of data from three modules connected in series.
"""

import matplotlib.pyplot as plt

from ecm import ModulesData
from utils import config_ax

# Battery modules US06 data
# ----------------------------------------------------------------------------

file_us06 = 'data/module123-ir-65ah-us06.csv'
data = ModulesData(file_us06)

data_proc = ModulesData(file_us06)
data_proc.process()

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.current)
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_proc.time, data_proc.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_proc.time, data_proc.current)
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

plt.show()
