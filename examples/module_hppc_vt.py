"""
Run equivalent circuit model (ECM) for battery module and compare to HPPC
data. Plot HPPC voltage data and ECM voltage. Plot absolute voltage difference
between HPPC data and ECM.
"""

import matplotlib.pyplot as plt

import params
from ecm import ModuleHppcData
from ecm import ModuleEcm
from utils import config_ax

# Data from HPPC battery module test and equivalent circuit model
# ----------------------------------------------------------------------------

file = 'data/module1-electchar-65ah-23deg.csv'
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
