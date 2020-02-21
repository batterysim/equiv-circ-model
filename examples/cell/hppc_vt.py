"""
Use HPPC battery cell data to develop a battery cell equivalent circuit model
(ECM). Compare the voltage profile of the cell ECM to HPPC battery cell data.
"""

import matplotlib.pyplot as plt

import params
from ecm import CellHppcData
from ecm import CellEcm
from ecm import config_ax

# Battery cell HPPC data and equivalent circuit model
# ----------------------------------------------------------------------------

file = '../data/cell-low-current-hppc-25c-2.csv'
data = CellHppcData(file)

ecm = CellEcm(data, params)
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
