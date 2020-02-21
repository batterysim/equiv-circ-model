"""
Use HPPC battery cell data to develop a cell ECM. Scale the cell ECM to
predict the voltage profile from HPPC battery module data. This script models
each battery cell individually.

The 2013 Nissan Leaf battery module consists of 4 cells in a 2P-2S
configuration such as:

             |== Cell ==|       |== Cell ==|
i_module  ---|          |---*---|          |---*
             |== Cell ==|       |== Cell ==|
"""

import matplotlib.pyplot as plt
import numpy as np

import params
from ecm import CellHppcData
from ecm import CellEcm
from ecm import ModuleHppcData
from ecm import config_ax

# ECM for battery cell
# ----------------------------------------------------------------------------

file_cell = '../data/cell-low-current-hppc-25c-2.csv'
data_cell = CellHppcData(file_cell)

ecm = CellEcm(data_cell, params)
ecm.q_cell = params.q_module / 2
soc = ecm.soc()
_, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)

coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Data from HPPC battery module test
# ----------------------------------------------------------------------------

file_module = '../data/module1-electchar-65ah-23deg.csv'
data_module = ModuleHppcData(file_module)

# Assume branch current is split evenly for two cells in parallel
# Calculate cell capacity from module capacity for two cells in parallel
ecm.current = data_module.current / 2
ecm.time = data_module.time
ecm.q_cell = params.q_module / 2

# Calculations for battery module
# ----------------------------------------------------------------------------

n_parallel = 2      # number of cells in parallel
n_series = 2        # number of cells in series

zi = np.ones((n_series, n_parallel))
ocv_cells = np.interp(zi, z_pts[::-1], v_pts[::-1])
r0_cells = rctau[:, 2].mean() * np.ones((n_series, n_parallel))

# current applied to battery module
i_module = data_module.current

i_cells = np.zeros((len(i_module), n_series, n_parallel))

for k in range(1, len(i_module)):
    v_modules = (np.sum(ocv_cells / r0_cells, axis=1) - i_module[k]) / np.sum(1 / r0_cells, axis=1)
    i_cells[k] = ((ocv_cells.T - v_modules).T) / r0_cells

i_cells2 = i_cells.transpose(1, 2, 0).reshape(i_cells[0].size, len(i_module))

n_cells = n_parallel * n_series
v_cells = np.zeros((n_cells, len(i_module)))

for k in range(n_cells):
    ecm.current = i_cells2[k]
    soc = ecm.soc()
    ocv = ecm.ocv(soc, vz_pts=(v_pts, z_pts))
    vt = ecm.vt(soc, ocv, rctau)
    v_cells[k] = vt

v_module = v_cells[0] * n_series

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_module.time, data_module.voltage, color='C3', label='data')
ax.plot(data_module.time, v_module, 'k--', label='ecm')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
for k in range(n_cells):
    ax.plot(data_module.time, v_cells[k] * 2, label=f'cell {k+1}')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

plt.show()
