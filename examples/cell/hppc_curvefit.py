"""
Use HPPC battery cell data to determine curve fit coefficients for each SOC
section. Curve fit coefficients are from one time constant (OTC) and two time
constant (TTC) functions.OTC represents one RC pair and TTC represents two RC
pairs.
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

# Print curve fit coefficients
# ----------------------------------------------------------------------------

func_otc = ecm.func_otc
func_ttc = ecm.func_ttc

coeffs_otc = ecm.curve_fit_coeff(func_otc, 3)
coeffs_ttc = ecm.curve_fit_coeff(func_ttc, 5)

print('\n--- Curve fit coefficients from OTC ---')
print('a\tb\talpha')
for c in coeffs_otc:
    print(f'{c[0]:.4f}\t{c[1]:.4f}\t{c[2]:.4f}')

print('\n--- Curve fit coefficients from TTC ---')
print('a\tb\tc\talpha\tbeta')
for c in coeffs_ttc:
    print(f'{c[0]:.4f}\t{c[1]:.4f}\t{c[2]:.4f}\t{c[3]:.4f}\t{c[4]:.4f}')
print('')

# Plot curve fit
# ----------------------------------------------------------------------------

# indices representing start (id2) and end (id4) of curve in each SOC section
_, _, id2, _, id4 = data.get_indices_discharge()

for i in range(len(id2)):
    start = id2[i]
    end = id4[i]
    t_curve = data.time[start:end]
    v_curve = data.voltage[start:end]
    t_scale = t_curve - t_curve[0]

    vfit1 = ecm.func_otc(t_scale, *coeffs_otc[i])
    vfit2 = ecm.func_ttc(t_scale, *coeffs_ttc[i])

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(t_curve, v_curve, 'C3', marker='.', label='data')
    ax.plot(t_curve, vfit1, label='otc')
    ax.plot(t_curve, vfit2, label='ttc')
    config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), title=f'SOC section {i}', loc='best')

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.voltage, 'C3', label='data')
ax.plot(data.time[id2], data.voltage[id2], 'x', label='id2')
ax.plot(data.time[id4], data.voltage[id4], 'x', label='id4')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'), loc='best')

plt.show()
