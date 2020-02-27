"""
Use HPPC battery module data to develop a module ECM. Use HPPC battery cell
data to develop a cell ECM. Scale the cell ECM to predict the voltage profile
from HPPC battery module data. This script uses one battery cell model to
predict a module.

Use ECM for a battery cell to predict battery module voltage. Compare cell and
module results using HPPC battery module data. Battery module consists of 4
cells in a 2P-2S configuration.

             |== Cell ==|       |== Cell ==|
i_module  ---|          |---*---|          |---*
             |== Cell ==|       |== Cell ==|
"""

import matplotlib.pyplot as plt

import params
from ecm import CellHppcData
from ecm import CellEcm
from ecm import ModuleHppcData
from ecm import ModuleEcm
from ecm import config_ax

# ECM for battery module
# ----------------------------------------------------------------------------

file_module = '../data/module1-electchar-65ah-23deg.csv'
data_module = ModuleHppcData(file_module)

ecm_module = ModuleEcm(data_module, params)

soc_module = ecm_module.soc()
ocv_module, _, _, vpts_module, zpts_module = ecm_module.ocv(soc_module, pts=True)
coeffs_module = ecm_module.curve_fit_coeff(ecm_module.func_ttc, 5)
rctau_module = ecm_module.rctau_ttc(coeffs_module)
vt_module = ecm_module.vt(soc_module, ocv_module, rctau_module)

# ECM for battery cell
# ----------------------------------------------------------------------------

file_cell = '../data/cell-low-current-hppc-25c-2.csv'
data_cell = CellHppcData(file_cell)

# Assume branch current is split evenly for two cells in parallel. Calculate
# cell capacity from module capacity for two cells in parallel. Use OCV and
# SOC points from ECM module to correctly calculate OCV from ECM cell.
ecm_cell = CellEcm(data_cell, params)
ecm_cell.current = data_module.current / 2
ecm_cell.time = data_module.time
ecm_cell.q_cell = params.q_module / 2

soc_cell = ecm_cell.soc()
ocv_cell = ecm_cell.ocv(soc_cell, vz_pts=(vpts_module, zpts_module))
# coeffs_cell = ecm_cell.curve_fit_coeff(ecm_cell.func_ttc, 5)
# rctau_cell = ecm_cell.rctau_ttc(coeffs_module)
vt_cell = ecm_cell.vt(soc_cell, ocv_cell, rctau_module)

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(ecm_module.time, soc_module, 'm', label='module')
ax.plot(ecm_cell.time, soc_cell, 'k--', label='cell')
config_ax(ax, xylabels=('Time [s]', 'State of charge [-]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(soc_module, ocv_module, 'C1', label='module')
ax.plot(zpts_module, vpts_module, 'C1o', label='module pts')
# ax.plot(soc_cell, ocv_cell * 2, 'k--', label='cell')
# ax.plot(zpts_cell, vpts_cell * 2, 'kx', label='cell pts')
config_ax(ax, xylabels=('State of charge [-]', 'Open circuit voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(ecm_module.time, vt_module, 'C3', label='module')
ax.plot(ecm_cell.time, vt_cell, 'k--', label='cell')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_module.time, data_module.voltage, 'C3', label='module data')
ax.plot(ecm_cell.time, vt_cell, 'k--', label='cell ecm')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_module.time, abs(data_module.voltage - vt_cell))
config_ax(ax, xylabels=('Time [s]', 'Absolute voltage difference [V]'))

plt.show()
