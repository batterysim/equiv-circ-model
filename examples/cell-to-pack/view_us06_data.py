"""
View plots of data from three modules connected in series. Data is provided by
NREL and represents a US06 drive cycle test.
"""

import matplotlib.pyplot as plt

from ecm import PackUs06Data
from ecm import config_ax

# Battery modules US06 data
# ----------------------------------------------------------------------------

# original data
file_us06 = '../data/module123-ir-65ah-us06.csv'
data = PackUs06Data(file_us06, all_data=True)

# processed data for 600s of US06 drive cycle
data_proc = PackUs06Data(file_us06)

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.current)
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.temp_a1, label='temp_a1')
ax.plot(data.time, data.temp_a2, label='temp_a2')
ax.plot(data.time, data.temp_a3, label='temp_a3')
config_ax(ax, xylabels=('Time [s]', 'Temperature [°C]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_proc.time, data_proc.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_proc.time, data_proc.current)
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_proc.time, data_proc.temp_a1, label='temp_a1')
ax.plot(data_proc.time, data_proc.temp_a2, label='temp_a2')
ax.plot(data_proc.time, data_proc.temp_a3, label='temp_a3')
config_ax(ax, xylabels=('Time [s]', 'Temperature [°C]'))

plt.show()
