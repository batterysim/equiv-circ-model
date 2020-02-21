"""
Use HPPC battery module data to develop a module ECM. Use HPPC battery cell
data to develop a cell ECM. Scale the cell ECM to predict the SOC and OCV of
the module ECM.

The 2013 Nissan Leaf battery module consists of 4 cells in a 2P-2S
configuration such as:

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

# Print
# ----------------------------------------------------------------------------

print(f'\nq_module = {ecm_module.q_module} Ah')
print(f'soc_module max = {max(soc_module):.4f}')
print(f'soc_module min = {min(soc_module):.4f}')

print('\nitem\tvpts\tzpts')
for i, (v, z) in enumerate(zip(vpts_module, zpts_module)):
    print(f'{i}\t{vpts_module[i]:.4f}\t{zpts_module[i]:.4f}')

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(ecm_module.time, soc_module, 'm', label='module')
ax.plot(ecm_cell.time, soc_cell, 'k--', label='cell')
config_ax(ax, xylabels=('Time [s]', 'State of charge [-]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(soc_module, ocv_module, 'C1', label='module')
ax.plot(zpts_module, vpts_module, 'C1o', label='module pts')
ax.plot(soc_cell, ocv_cell, 'k--', label='cell')
config_ax(ax, xylabels=('State of charge [-]', 'Open circuit voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(ecm_module.time, ocv_module, 'C1', label='module')
ax.plot(ecm_cell.time, ocv_cell, 'k--', label='cell')
config_ax(ax, xylabels=('Time [s]', 'Open circuit voltage [V]'), loc='best')

plt.show()
