"""
Use HPPC battery cell data to develop a cell ECM. Use the cell ECM to predict
battery pack voltage. The battery pack is represented by 3 modules in series
where each module contains 4 cells in a 2P-2S configuration. Cells and modules
(pack) data are from a 2013 Nissan Leaf. The battery pack data is from a US06
drive cycle test.

           |== Cell ==|  |== Cell ==|
Module  ---|          |--|          |---
           |== Cell ==|  |== Cell ==|

         |            |  |            |  |            |
Pack  ---|== Module ==|--|== Module ==|--|== Module ==|---
         |            |  |            |  |            |
"""

import matplotlib.pyplot as plt

import params
from ecm import CellEcm
from ecm import CellHppcData
from ecm import PackUs06Data
from ecm import config_ax

# Parameters
# ----------------------------------------------------------------------------

n_parallel = 2

# Data
# ----------------------------------------------------------------------------

# data from US06 drive cycle test where 3 modules in series is a pack
file_us06 = '../data/module123-ir-65ah-us06.csv'
data_us06 = PackUs06Data(file_us06)

# data from HPPC battery cell test
file_hppc = '../data/cell-low-current-hppc-25c-2.csv'
data_hppc = CellHppcData(file_hppc)

# ECM battery cell
# ----------------------------------------------------------------------------

ecm = CellEcm(data_hppc, params)
soc = ecm.soc()
_, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)
coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Cell ECM to pack calculations
# ----------------------------------------------------------------------------

ecm.current = data_us06.current / n_parallel
ecm.time = data_us06.time
ecm.q_cell = params.q_module / n_parallel

soc = ecm.soc()
ocv = ecm.ocv(soc, vz_pts=(v_pts, z_pts))
vt = ecm.vt(soc, ocv, rctau)

vt_pack = vt * 5.965

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_us06.time, data_us06.voltage, color='C3', label='pack data')
ax.plot(data_us06.time, vt_pack, color='k', label='cell ecm')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_us06.time, abs(data_us06.voltage - vt_pack))
config_ax(ax, xylabels=('Time [s]', 'Absolute voltage difference [V]'))

plt.show()
