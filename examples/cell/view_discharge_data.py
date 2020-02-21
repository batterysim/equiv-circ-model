"""
View plots of the battery cell discharge electrical data and associated
temperature data.
"""

import matplotlib.pyplot as plt

from ecm import CellDischargeData
from ecm import CellTemperatureData
from ecm import config_ax

# Data files
# ----------------------------------------------------------------------------

file_dis_1c = '../data/cell-discharge-bitrode-1c.csv'
file_dis_2c = '../data/cell-discharge-bitrode-2c.csv'
file_dis_3c = '../data/cell-discharge-bitrode-3c.csv'

file_temp_1c = '../data/cell-discharge-temperature-1c.lvm'
file_temp_2c = '../data/cell-discharge-temperature-2c.lvm'
file_temp_3c = '../data/cell-discharge-temperature-3c.lvm'

# Original cell discharge data
# ----------------------------------------------------------------------------

dis_1c = CellDischargeData(file_dis_1c)
dis_2c = CellDischargeData(file_dis_2c)
dis_3c = CellDischargeData(file_dis_3c)

temp_1c = CellTemperatureData(file_temp_1c, dis_1c.ti, dis_1c.tf)
temp_2c = CellTemperatureData(file_temp_2c, dis_2c.ti, dis_2c.tf)
temp_3c = CellTemperatureData(file_temp_3c, dis_3c.ti, dis_3c.tf)

# Processed cell discharge data
# ----------------------------------------------------------------------------

dis_1c_proc = CellDischargeData.process(file_dis_1c)
dis_2c_proc = CellDischargeData.process(file_dis_2c)
dis_3c_proc = CellDischargeData.process(file_dis_3c)

temp_1c_proc = CellTemperatureData.process(file_temp_1c, dis_1c_proc.ti, dis_1c_proc.tf)
temp_2c_proc = CellTemperatureData.process(file_temp_2c, dis_2c_proc.ti, dis_2c_proc.tf)
temp_3c_proc = CellTemperatureData(file_temp_3c, dis_3c_proc.ti, dis_3c_proc.tf)

# Processed cell discharge data for just the discharge section
# ----------------------------------------------------------------------------

dis_1c_sect = CellDischargeData.process_discharge_only(file_dis_1c)
dis_2c_sect = CellDischargeData.process_discharge_only(file_dis_2c)
dis_3c_sect = CellDischargeData.process_discharge_only(file_dis_3c)

temp_1c_sect = CellTemperatureData.process(file_temp_1c, dis_1c_sect.ti, dis_1c_sect.tf)
temp_2c_sect = CellTemperatureData.process(file_temp_2c, dis_2c_sect.ti, dis_2c_sect.tf)
temp_3c_sect = CellTemperatureData.process(file_temp_3c, dis_3c_sect.ti, dis_3c_sect.tf)

# Plot original data
# ----------------------------------------------------------------------------

# original current data
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 4.8), sharey=True, tight_layout=True)
ax1.plot(dis_1c.time, dis_1c.current)
ax2.plot(dis_2c.time, dis_2c.current)
ax3.plot(dis_3c.time, dis_3c.current)
config_ax(ax1, xylabels=('', 'Current [A]'))
config_ax(ax2, xylabels=('Time [s]', ''))
config_ax(ax3)

# original voltage data
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 4.8), sharey=True, tight_layout=True)
ax1.plot(dis_1c.time, dis_1c.voltage, color='C3')
ax2.plot(dis_2c.time, dis_2c.voltage, color='C3')
ax3.plot(dis_3c.time, dis_3c.voltage, color='C3')
config_ax(ax1, xylabels=('', 'Voltage [V]'))
config_ax(ax2, xylabels=('Time [s]', ''))
config_ax(ax3)

# original temperature data
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

# Plot processed data
# ----------------------------------------------------------------------------

# processed data and discharge section data for current
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
ax1.plot(dis_1c_proc.time, dis_1c_proc.current, marker='.', label='1c')
ax1.plot(dis_2c_proc.time, dis_2c_proc.current, marker='.', label='2c')
ax1.plot(dis_3c_proc.time, dis_3c_proc.current, marker='.', label='3c')
config_ax(ax1, xylabels=('Time [s]', 'Current [A]'), loc='lower right')
ax2.plot(dis_1c_sect.time, dis_1c_sect.current, marker='.', label='1c')
ax2.plot(dis_2c_sect.time, dis_2c_sect.current, marker='.', label='2c')
ax2.plot(dis_3c_sect.time, dis_3c_sect.current, marker='.', label='3c')
config_ax(ax2, xylabels=('Time [s]', 'Current [A]'), loc='lower right')

# processed data and discharge section data for voltage
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
ax1.plot(dis_1c_proc.time, dis_1c_proc.voltage, marker='.', label='1c')
ax1.plot(dis_2c_proc.time, dis_2c_proc.voltage, marker='.', label='2c')
ax1.plot(dis_3c_proc.time, dis_3c_proc.voltage, marker='.', label='3c')
config_ax(ax1, xylabels=('Time [s]', 'Voltage [V]'), loc='upper right')
ax2.plot(dis_1c_sect.time, dis_1c_sect.voltage, marker='.', label='1c')
ax2.plot(dis_2c_sect.time, dis_2c_sect.voltage, marker='.', label='2c')
ax2.plot(dis_3c_sect.time, dis_3c_sect.voltage, marker='.', label='3c')
config_ax(ax2, xylabels=('Time [s]', 'Voltage [V]'), loc='upper right')

# processed data and discharge section data for 1C temperatures
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
ax1.plot(temp_1c_proc.time, temp_1c_proc.tc1, label='tc1')
ax1.plot(temp_1c_proc.time, temp_1c_proc.tc2, label='tc2')
ax1.plot(temp_1c_proc.time, temp_1c_proc.tc3, label='tc3')
ax1.plot(temp_1c_proc.time, temp_1c_proc.tc4, label='tc4')
ax1.plot(temp_1c_proc.time, temp_1c_proc.tavg, 'k', label='tavg')
config_ax(ax1, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')
ax2.plot(temp_1c_sect.time, temp_1c_sect.tc1, label='tc1')
ax2.plot(temp_1c_sect.time, temp_1c_sect.tc2, label='tc2')
ax2.plot(temp_1c_sect.time, temp_1c_sect.tc3, label='tc3')
ax2.plot(temp_1c_sect.time, temp_1c_sect.tc4, label='tc4')
ax2.plot(temp_1c_sect.time, temp_1c_sect.tavg, 'k', label='tavg')
config_ax(ax2, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')

# processed data and discharge section data for 2C temperatures
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
ax1.plot(temp_2c_proc.time, temp_2c_proc.tc1, label='tc1')
ax1.plot(temp_2c_proc.time, temp_2c_proc.tc2, label='tc2')
ax1.plot(temp_2c_proc.time, temp_2c_proc.tc3, label='tc3')
ax1.plot(temp_2c_proc.time, temp_2c_proc.tc4, label='tc4')
ax1.plot(temp_2c_proc.time, temp_2c_proc.tavg, 'k', label='tavg')
config_ax(ax1, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')
ax2.plot(temp_2c_sect.time, temp_2c_sect.tc1, label='tc1')
ax2.plot(temp_2c_sect.time, temp_2c_sect.tc2, label='tc2')
ax2.plot(temp_2c_sect.time, temp_2c_sect.tc3, label='tc3')
ax2.plot(temp_2c_sect.time, temp_2c_sect.tc4, label='tc4')
ax2.plot(temp_2c_sect.time, temp_2c_sect.tavg, 'k', label='tavg')
config_ax(ax2, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')

# processed data and discharge section data for 3C temperatures
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
ax1.plot(temp_3c_proc.time, temp_3c_proc.tc1, label='tc1')
ax1.plot(temp_3c_proc.time, temp_3c_proc.tc2, label='tc2')
ax1.plot(temp_3c_proc.time, temp_3c_proc.tc3, label='tc3')
ax1.plot(temp_3c_proc.time, temp_3c_proc.tc4, label='tc4')
ax1.plot(temp_3c_proc.time, temp_3c_proc.tavg, 'k', label='tavg')
config_ax(ax1, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')
ax2.plot(temp_3c_sect.time, temp_3c_sect.tc1, label='tc1')
ax2.plot(temp_3c_sect.time, temp_3c_sect.tc2, label='tc2')
ax2.plot(temp_3c_sect.time, temp_3c_sect.tc3, label='tc3')
ax2.plot(temp_3c_sect.time, temp_3c_sect.tc4, label='tc4')
ax2.plot(temp_3c_sect.time, temp_3c_sect.tavg, 'k', label='tavg')
config_ax(ax2, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper left')

# compared processed data and discharge section data for 1C, 2C, 3C temperatures
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), tight_layout=True)
ax1.plot(temp_1c_proc.time, temp_1c_proc.tavg, marker='.', markevery=20, label='1c')
ax1.plot(temp_2c_proc.time, temp_2c_proc.tavg, marker='.', markevery=20, label='2c')
ax1.plot(temp_3c_proc.time, temp_3c_proc.tavg, marker='.', markevery=20, label='3c')
ax1.fill_between(temp_1c_proc.time, temp_1c_proc.tmax, temp_1c_proc.tmin, alpha=0.3)
ax1.fill_between(temp_2c_proc.time, temp_2c_proc.tmax, temp_2c_proc.tmin, alpha=0.3)
ax1.fill_between(temp_3c_proc.time, temp_3c_proc.tmax, temp_3c_proc.tmin, alpha=0.3)
config_ax(ax1, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper right')
ax2.plot(temp_1c_sect.time, temp_1c_sect.tavg, marker='.', markevery=20, label='1c')
ax2.plot(temp_2c_sect.time, temp_2c_sect.tavg, marker='.', markevery=20, label='2c')
ax2.plot(temp_3c_sect.time, temp_3c_sect.tavg, marker='.', markevery=20, label='3c')
ax2.fill_between(temp_1c_sect.time, temp_1c_sect.tmax, temp_1c_sect.tmin, alpha=0.3)
ax2.fill_between(temp_2c_sect.time, temp_2c_sect.tmax, temp_2c_sect.tmin, alpha=0.3)
ax2.fill_between(temp_3c_sect.time, temp_3c_sect.tmax, temp_3c_sect.tmin, alpha=0.3)
config_ax(ax2, xylabels=('Time [s]', 'Temperature [°C]'), loc='upper right')

plt.show()
