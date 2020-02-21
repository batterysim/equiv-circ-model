"""
Use HPPC battery module data to develop a battery cell equivalent circuit
model (ECM). Compare the voltage profile of the cell ECM to the HPPC battery
module data.
"""

import matplotlib.pyplot as plt

import params
from ecm import ModuleHppcData
from ecm import ModuleEcm
from ecm import config_ax

# Data from HPPC battery module test and equivalent circuit model
# ----------------------------------------------------------------------------

file = '../data/module1-electchar-65ah-23deg.csv'
data = ModuleHppcData(file)

ecm = ModuleEcm(data, params)
soc = ecm.soc()
ocv = ecm.ocv(soc)
coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)
vt = ecm.vt(soc, ocv, rctau)

# Plot HPPC data and equivalent circuit model
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.voltage, 'C3', label='data')
ax.plot(data.time, vt, 'k--', label='ecm')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, abs(data.voltage - vt))
config_ax(ax, xylabels=('Time [s]', 'Absolute voltage difference [V]'))

plt.show()
