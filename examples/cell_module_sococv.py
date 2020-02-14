"""
Use ECM for a battery cell to predict SOC and OCV for a battery module.
Compare cell and module results using HPPC battery module data. Battery module
consists of 4 cells in a 2P-2S configuration.

             |== Cell ==|       |== Cell ==|
i_module  ---|          |---*---|          |---*
             |== Cell ==|       |== Cell ==|
"""

import matplotlib.pyplot as plt

import params
from utils import config_ax
from ecm import CellHppcData
from ecm import CellEcm
from ecm import ModuleHppcData
from ecm import ModuleEcm

# ECM for battery module
# ----------------------------------------------------------------------------

file_module = 'data/module1-electchar-65ah-23deg.csv'
data_module = ModuleHppcData(file_module)

ecm_module = ModuleEcm(data_module, params)

soc_module = ecm_module.soc()
ocv_module, _, _, vpts_module, zpts_module = ecm_module.ocv(soc_module, pts=True)

# ECM for battery cell
# ----------------------------------------------------------------------------

file_cell = 'data/cell-low-current-hppc-25c-2.csv'
data_cell = CellHppcData(file_cell)

ecm_cell = CellEcm(data_cell, params)
ecm_cell.q_cell = params.q_module / 2

soc_cell = ecm_cell.soc()
_, _, _, vpts_cell, zpts_cell = ecm_cell.ocv(soc_cell, pts=True)

# Assume branch current is split evenly for two cells in parallel
# Calculate cell capacity from module capacity for two cells in parallel
ecm_cell.current = data_module.current / 2
ecm_cell.time = data_module.time
# ecm_cell.q_cell = params.q_module / 2

soc_cell2 = ecm_cell.soc()
# zpts_cell[-1] = soc_cell2[-1]
vpts_cell2 = vpts_cell * 2
ocv_cell2 = ecm_cell.ocv(soc_cell2, vz_pts=(vpts_cell2, zpts_cell))

# Print
# ----------------------------------------------------------------------------

print(f'\nq_module = {ecm_module.q_module} Ah')
print(f'soc_module max = {max(soc_module):.4f}')
print(f'soc_module min = {min(soc_module):.4f}')

print('\nitem\tvpts\tzpts')
for i, (v, z) in enumerate(zip(vpts_module, zpts_module)):
    print(f'{i}\t{vpts_module[i]:.4f}\t{zpts_module[i]:.4f}')

print(f'\nq_cell = {ecm_cell.q_cell} Ah')
print(f'soc_cell2 max = {max(soc_cell2):.4f}')
print(f'soc_cell2 min = {min(soc_cell2):.4f}')

print('\nitem\tvpts\tzpts')
for i, (v, z) in enumerate(zip(vpts_cell, zpts_cell)):
    print(f'{i}\t{vpts_cell[i]:.4f}\t{zpts_cell[i]:.4f}')
print('')

print('\nitem\tvpts2\tzpts')
for i, (v, z) in enumerate(zip(vpts_cell2, zpts_cell)):
    print(f'{i}\t{vpts_cell2[i]:.4f}\t{zpts_cell[i]:.4f}')
print('')

# Plot
# ----------------------------------------------------------------------------

# fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4.8), tight_layout=True)
# ax1.plot(data_module.time, data_module.voltage, 'C3')
# config_ax(ax1, xylabels=('Time [s]', 'Voltage [V]'), title='Module')
# ax2.plot(data_cell.time, data_cell.voltage, 'C3')
# config_ax(ax2, xylabels=('Time [s]', 'Voltage [V]'), title='Cell')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(ecm_module.time, soc_module, 'm', label='module')
ax.plot(ecm_cell.time, soc_cell2, 'k--', label='cell')
ax.plot(data_cell.time, soc_cell, label='cell hppc')
config_ax(ax, xylabels=('Time [s]', 'State of charge [-]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(soc_module, ocv_module, 'C1', label='module')
ax.plot(zpts_module, vpts_module, 'C1o', label='module pts')
ax.plot(soc_cell2, ocv_cell2, 'k--', label='cell')
ax.plot(zpts_cell, vpts_cell2, 'kx', label='cell pts')
config_ax(ax, xylabels=('State of charge [-]', 'Open circuit voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(ecm_module.time, ocv_module, 'C1', label='module')
ax.plot(ecm_cell.time, ocv_cell2, 'k--', label='cell')
config_ax(ax, xylabels=('Time [s]', 'Open circuit voltage [V]'), loc='best')

plt.show()
