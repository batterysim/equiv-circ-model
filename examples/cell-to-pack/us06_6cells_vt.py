"""
Use HPPC battery cell data to develop a cell ECM. Configure the cell model to
represent a battery pack with 6 cells. Apply a US06 drive cycle current to the
battery pack model. Each cell in the battery pack is initialized with a random
SOC. Finally, plot the results for each battery cell model which represents
each cell in the battery pack.

Battery pack where cells are connected in parallel to make a module. The
modules are connected in series to make a pack.

         |== Cell ==|     |== Cell ==|
Pack  ---|== Cell ==|--*--|== Cell ==|---
         |== Cell ==|     |== Cell ==|
"""

import matplotlib.pyplot as plt
import numpy as np

import params
from ecm import CellHppcData
from ecm import CellEcm
from ecm import PackUs06Data
from ecm import ThermalModel
from ecm import config_ax

# ECM for battery cell
# ----------------------------------------------------------------------------

file_hppc = '../data/cell-low-current-hppc-25c-2.csv'
data_hppc = CellHppcData(file_hppc)

ecm = CellEcm(data_hppc, params)
soc = ecm.soc()
_, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)

coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Data from US06 battery modules (pack) drive cycle test
# ----------------------------------------------------------------------------

file_us06 = '../data/module123-ir-65ah-us06.csv'
data_us06 = PackUs06Data(file_us06)

ecm.current = data_us06.current
ecm.voltage = data_us06.voltage
ecm.time = data_us06.time

# soc_dis = ecm.soc()
# ocv_dis = ecm.ocv(soc_dis, vz_pts=(v_pts, z_pts))
# vt_dis = ecm.vt(soc_dis, ocv_dis, rctau)

# Calculations for battery pack
# ----------------------------------------------------------------------------

n_parallel = 3      # number of cells in parallel to make a module
n_series = 2        # number of battery modules in series to make a pack

# initial random state of charge (SOC) for each cell, zi units of [-]
zi = np.random.uniform(0.95, 1.00, (n_series, n_parallel))

# initial random capacity (Q) for each cell, qi units of [Ah]
# qi = np.random.uniform(29, 30.7, (n_series, n_parallel))

# total capacity [Ah] of battery pack
# pack capacity is the minimum module capacity
# q_pack = min(np.sum(qi, axis=1))

ocv_cells = np.interp(zi, z_pts[::-1], v_pts[::-1])
r0_cells = rctau[:, 2].mean() * np.ones((n_series, n_parallel))

# current [A] applied to battery pack at 3C discharge rate
i_pack = ecm.current * 3

i_cells = np.zeros((len(i_pack), n_series, n_parallel))

for k in range(1, len(i_pack)):
    v_modules = (np.sum(ocv_cells / r0_cells, axis=1) - i_pack[k]) / np.sum(1 / r0_cells, axis=1)
    i_cells[k] = ((ocv_cells.T - v_modules).T) / r0_cells

i_cells2 = i_cells.transpose(1, 2, 0).reshape(i_cells[0].size, len(i_pack))

n_cells = n_parallel * n_series
v_cells = np.zeros((n_cells, len(i_pack)))
temp_cells = np.zeros((n_cells, len(i_pack)))

tm = ThermalModel(params)

for k in range(n_cells):
    ecm.current = i_cells2[k]
    soc = ecm.soc()
    ocv = ecm.ocv(soc, vz_pts=(v_pts, z_pts))
    vt = ecm.vt(soc, ocv, rctau)
    v_cells[k] = vt

    icell = i_cells2[k]
    _, temp_cell = tm.calc_q_temp(i=icell, ocv=ocv, time=data_us06.time, ti=297, vt=vt)
    temp_cells[k] = temp_cell

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_us06.time, data_us06.current)
config_ax(ax, xylabels=('Time [s]', 'Current [A]'))

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_us06.time, data_us06.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

fig, ax = plt.subplots(tight_layout=True)
for k in range(n_cells):
    ax.plot(data_us06.time, i_cells2[k], label=f'cell {k+1}')
config_ax(ax, xylabels=('Time [s]', 'Current [A]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
for k in range(n_cells):
    ax.plot(data_us06.time, v_cells[k], label=f'cell {k+1}')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
for k in range(n_cells):
    ax.plot(data_us06.time, temp_cells[k], label=f'cell {k+1}')
config_ax(ax, xylabels=('Time [s]', 'Temperature [K]'), loc='best')

plt.show()
