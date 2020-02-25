"""
here

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
from ecm import ModuleEcm
from ecm import ModuleHppcData
from ecm import PackUs06Data
from ecm import config_ax
from helpers import get_vt_cell_pack
from helpers import get_vt_module_pack
from helpers import r2fit

# Parameters
# ----------------------------------------------------------------------------

n_parallel = 2

# Data
# ----------------------------------------------------------------------------

# data from US06 drive cycle test where 3 modules in series is a pack
data_us06 = PackUs06Data('../data/module123-ir-65ah-us06.csv')

# data from HPPC battery cell test
data_hppc_cell = CellHppcData('../data/cell-low-current-hppc-25c-2.csv')

# data from HPPC battery module test
data_hppc_mod = ModuleHppcData('../data/module1-electchar-65ah-23deg.csv')

# ECM battery cell
# ----------------------------------------------------------------------------

ecm_cell = CellEcm(data_hppc_cell, params)
vt_cell = get_vt_cell_pack(params, n_parallel, data_us06, ecm_cell)

# ECM battery module
# ----------------------------------------------------------------------------

ecm_module = ModuleEcm(data_hppc_mod, params)
vt_module = get_vt_module_pack(data_us06, ecm_module)

# Print
# ----------------------------------------------------------------------------

r2_cell = r2fit(data_us06.voltage, vt_cell)
r2_module = r2fit(data_us06.voltage, vt_module)

print(f'R² cell    {r2_cell:.2f}')
print(f'R² module  {r2_module:.2f}')

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_us06.time, data_us06.voltage, color='C3', label='pack data')
ax.plot(data_us06.time, vt_cell, color='k', label='cell ecm')
ax.plot(data_us06.time, vt_module, color='m', label='module ecm')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_us06.time, abs(data_us06.voltage - vt_cell), label='cell ecm')
ax.plot(data_us06.time, abs(data_us06.voltage - vt_module), label='module ecm')
config_ax(ax, xylabels=('Time [s]', 'Absolute voltage difference [V]'), loc='best')

plt.show()
