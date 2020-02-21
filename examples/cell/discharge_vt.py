"""
Use HPPC battery cell data to develop a battery cell ECM. Apply current from
the 1C, 2C, and 3C battery cell discharge tests to the cell model. Compare the
cell model to the discharge voltage and temperature data.
"""

import matplotlib.pyplot as plt

import params
from ecm import CellDischargeData
from ecm import CellTemperatureData
from ecm import CellHppcData
from ecm import CellEcm
from ecm import ThermalModel
from ecm import config_ax

# Data files
# ----------------------------------------------------------------------------

file_hppc = '../data/cell-low-current-hppc-25c-2.csv'

file_dis_1c = '../data/cell-discharge-bitrode-1c.csv'
file_dis_2c = '../data/cell-discharge-bitrode-2c.csv'
file_dis_3c = '../data/cell-discharge-bitrode-3c.csv'

file_temp_1c = '../data/cell-discharge-temperature-1c.lvm'
file_temp_2c = '../data/cell-discharge-temperature-2c.lvm'
file_temp_3c = '../data/cell-discharge-temperature-3c.lvm'

# Processed cell discharge data for just the discharge section
# ----------------------------------------------------------------------------

dis_1c = CellDischargeData.process_discharge_only(file_dis_1c)
dis_2c = CellDischargeData.process_discharge_only(file_dis_2c)
dis_3c = CellDischargeData.process_discharge_only(file_dis_3c)

temp_1c = CellTemperatureData.process(file_temp_1c, dis_1c.ti, dis_1c.tf)
temp_2c = CellTemperatureData.process(file_temp_2c, dis_2c.ti, dis_2c.tf)
temp_3c = CellTemperatureData.process(file_temp_3c, dis_3c.ti, dis_3c.tf)

# Electrical model from HPPC cell data
# ----------------------------------------------------------------------------

data = CellHppcData(file_hppc)

ecm = CellEcm(data, params)
soc = ecm.soc()
_, _, _, v_pts, z_pts = ecm.ocv(soc, pts=True)
coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Thermal model from Discharge 1C
# ----------------------------------------------------------------------------

ecm.current = dis_1c.current
ecm.voltage = dis_1c.voltage
ecm.time = dis_1c.time
soc_1c = ecm.soc()
ocv_1c = ecm.ocv(soc_1c, vz_pts=(v_pts, z_pts))
vt_1c = ecm.vt(soc_1c, ocv_1c, rctau)

ti_1c = temp_1c.tc4.iloc[0] + 273.15

tm_1c = ThermalModel(params)
q_1c, tk_1c = tm_1c.calc_q_temp(i=dis_1c.current, ocv=ocv_1c, time=dis_1c.time, ti=ti_1c, vt=vt_1c)

# Thermal model from Discharge 2C
# ----------------------------------------------------------------------------

ecm.current = dis_2c.current
ecm.voltage = dis_2c.voltage
ecm.time = dis_2c.time
soc_2c = ecm.soc()
ocv_2c = ecm.ocv(soc_2c, vz_pts=(v_pts, z_pts))
vt_2c = ecm.vt(soc_2c, ocv_2c, rctau)

ti_2c = temp_2c.tc4.iloc[0] + 273.15

tm_2c = ThermalModel(params)
q_2c, tk_2c = tm_2c.calc_q_temp(i=dis_2c.current, ocv=ocv_2c, time=dis_2c.time, ti=ti_2c, vt=vt_2c)

# Thermal model from Discharge 3C
# ----------------------------------------------------------------------------

ecm.current = dis_3c.current
ecm.voltage = dis_3c.voltage
ecm.time = dis_3c.time
soc_3c = ecm.soc()
ocv_3c = ecm.ocv(soc_3c, vz_pts=(v_pts, z_pts))
vt_3c = ecm.vt(soc_3c, ocv_3c, rctau)

ti_3c = temp_3c.tc4.iloc[0] + 273.15

tm_3c = ThermalModel(params)
q_3c, tk_3c = tm_3c.calc_q_temp(i=dis_3c.current, ocv=ocv_3c, time=dis_3c.time, ti=ti_3c, vt=vt_3c)

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots()
ax.plot(dis_1c.time, dis_1c.voltage, marker='.', label='1c')
ax.plot(dis_2c.time, dis_2c.voltage, marker='.', label='2c')
ax.plot(dis_3c.time, dis_3c.voltage, marker='.', label='3c')
ax.plot(dis_1c.time, vt_1c, label='vt_1c')
ax.plot(dis_2c.time, vt_2c, label='vt_2c')
ax.plot(dis_3c.time, vt_3c, label='vt_3c')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='upper right')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(temp_1c.time, temp_1c.tavg + 273.15, marker='.', markevery=20, label='1c')
ax.plot(temp_2c.time, temp_2c.tavg + 273.15, marker='.', markevery=20, label='2c')
ax.plot(temp_3c.time, temp_3c.tavg + 273.15, marker='.', markevery=20, label='3c')
ax.fill_between(temp_1c.time, temp_1c.tmax + 273.15, temp_1c.tmin + 273.15, alpha=0.3)
ax.fill_between(temp_2c.time, temp_2c.tmax + 273.15, temp_2c.tmin + 273.15, alpha=0.3)
ax.fill_between(temp_3c.time, temp_3c.tmax + 273.15, temp_3c.tmin + 273.15, alpha=0.3)
ax.plot(dis_1c.time, tk_1c, label='tk_1c')
ax.plot(dis_2c.time, tk_2c, label='tk_2c')
ax.plot(dis_3c.time, tk_3c, label='tk_3c')
config_ax(ax, xylabels=('Time [s]', 'Temperature [K]'), loc='upper right')

plt.show()
