"""
"""

import matplotlib.pyplot as plt

import params
from ecm import ModulesData
from ecm import ModuleHppcData
from ecm import ModuleEcm
from utils import config_ax

# Data from US06 drive cycle
# ----------------------------------------------------------------------------

file = 'data/module123-ir-65ah-us06.csv'
data = ModulesData(file)
data.process()

# Data from HPPC battery module test and equivalent circuit model
# ----------------------------------------------------------------------------

file_hppc = 'data/module1-electchar-65ah-23deg.csv'
data_hppc = ModuleHppcData(file_hppc)

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

vt = vt * 3
# vt_modules = vt * 3

# Print
# ----------------------------------------------------------------------------

print('q =', ecm.q_module)

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, soc)
config_ax(ax, xylabels=('Time [s]', 'State of charge [-]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.voltage, 'C3')
ax.plot(data.time, vt)
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
