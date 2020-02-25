"""
Use HPPC battery module data to develop a module ECM. Configure the module
model to represent a battery pack where 3 modules are in series. Apply a US06
drive cycle current to the battery pack model. Finally, compare the results to
the US06 drive cycle data which is from three 2013 Nissan Leaf modules
connected in series.

           |            |     |            |     |            |
i_pack  ---|== Module ==|--*--|== Module ==|--*--|== Module ==|---
           |            |     |            |     |            |
"""

import matplotlib.pyplot as plt

import params
from ecm import PackUs06Data
from ecm import ModuleHppcData
from ecm import ModuleEcm
from ecm import config_ax

# Data
# ----------------------------------------------------------------------------

# data from US06 drive cycle from three modules in series
file = '../data/module123-ir-65ah-us06.csv'
data = PackUs06Data(file)

# data from HPPC battery module test
file_hppc = '../data/module1-electchar-65ah-23deg.csv'
data_hppc = ModuleHppcData(file_hppc)

# Module ECM
# ----------------------------------------------------------------------------

ecm = ModuleEcm(data_hppc, params)
soc = ecm.soc()
_, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)
coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Predict US06 drive cycle
# ----------------------------------------------------------------------------

ecm.current = data.current
ecm.time = data.time
soc = ecm.soc()
ocv = ecm.ocv(soc, vz_pts=(v_pts, z_pts))
vt = ecm.vt(soc, ocv, rctau)

temps = ecm.calc_temperature(295.15, ocv, vt)

# vt = vt * 3
vt = vt * 2.985

# Print
# ----------------------------------------------------------------------------

print('q =', ecm.q_module)

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, soc, 'C6')
config_ax(ax, xylabels=('Time [s]', 'State of charge [-]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.voltage, 'C3', label='data')
ax.plot(data.time, vt, 'k', label='ecm')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, abs(data.voltage - vt))
config_ax(ax, xylabels=('Time [s]', 'Absolute voltage difference [V]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.temp_a1 + 273.15)
ax.plot(data.time, data.temp_a2 + 273.15)
ax.plot(data.time, data.temp_a3 + 273.15)
ax.plot(data.time, temps)
config_ax(ax, xylabels=('Time [s]', 'Temperature [°C]'))

plt.show()
