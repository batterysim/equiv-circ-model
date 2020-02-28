"""
Use HPPC battery cell data to develop a cell ECM. Configure the cell model to
represent a battery pack with 6 cells. Apply a 3C current from a discharge
test to the battery pack. Each cell in the battery pack is initialized with a
random SOC. Finally, plot the results for each battery cell model which
represents each cell in the battery pack.

Battery pack where cells are connected in parallel to make a module. The
modules are connected in series to make a pack.

         |== Cell ==|     |== Cell ==|
Pack  ---|== Cell ==|--*--|== Cell ==|---
         |== Cell ==|     |== Cell ==|
"""

import matplotlib.pyplot as plt
import numpy as np

import params
from ecm import CellDischargeData
from ecm import CellHppcData
from ecm import CellEcm
from ecm import ThermalModel
from ecm import config_ax

# Battery cell ECM from battery cell HPPC data
# ----------------------------------------------------------------------------

file_hppc = '../data/cell-low-current-hppc-25c-2.csv'
data_hppc = CellHppcData(file_hppc)

ecm = CellEcm(data_hppc, params)
soc = ecm.soc()
_, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)

coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Battery cell discharge data
# ----------------------------------------------------------------------------

file_dis = '../data/cell-discharge-bitrode-1c.csv'
data_dis = CellDischargeData.process_discharge_only(file_dis)

ecm.current = data_dis.current
ecm.voltage = data_dis.voltage
ecm.time = data_dis.time

soc_dis = ecm.soc()
ocv_dis = ecm.ocv(soc_dis, vz_pts=(v_pts, z_pts))
vt_dis = ecm.vt(soc_dis, ocv_dis, rctau)

# Battery pack calculations
# ----------------------------------------------------------------------------

n_parallel = params.n_parallel
n_series = params.n_series

# initial random state of charge (SOC) for each cell, zi units of [-]
zi = np.random.uniform(0.95, 1.00, (n_series, n_parallel))

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
    _, temp_cell = tm.calc_q_temp(i=icell, ocv=ocv, time=data_dis.time, ti=297, vt=vt)
    temp_cells[k] = temp_cell

# Print
# ----------------------------------------------------------------------------

# currents for each cell in a module should sum to total discharge current
print(f'i_pack = {i_pack[-1]:.2f}')
print(f'i_sum0 = {i_cells[-1][0].sum():.2f}')
print(f'i_sum1 = {i_cells[-1][1].sum():.2f}')

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data_dis.time, data_dis.voltage, color='C3', marker='.', label='data')
ax.plot(data_dis.time, vt_dis, label='ecm')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, (ax1, ax2) = plt.subplots(1, 2, tight_layout=True)
ax1.plot(data_dis.time, i_pack, label='data')
config_ax(ax1, xylabels=('Time [s]', 'Current [A]'), loc='best')
for k in range(n_cells):
    ax2.plot(data_dis.time, i_cells2[k], label=f'cell {k+1}')
config_ax(ax2, xylabels=('Time [s]', ''), loc='best')

fig, ax = plt.subplots(tight_layout=True)
for k in range(n_cells):
    ax.plot(data_dis.time, v_cells[k], label=f'cell {k+1}')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

fig, ax = plt.subplots(tight_layout=True)
for k in range(n_cells):
    ax.plot(data_dis.time, temp_cells[k], label=f'cell {k+1}')
config_ax(ax, xylabels=('Time [s]', 'Temperature [K]'), loc='best')

plt.show()
