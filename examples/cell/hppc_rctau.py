"""
Use HPPC battery cell data to determine the tau, resistor and capacitor values
(RC parameters) for each SOC section. Curve fit coefficients are determined
from the two time constant (TTC) function.
"""

import params
from ecm import CellHppcData
from ecm import CellEcm

# Battery cell HPPC data and equivalent circuit model
# ----------------------------------------------------------------------------

file = '../data/cell-low-current-hppc-25c-2.csv'
data = CellHppcData(file)

ecm = CellEcm(data, params)
coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Print curve fit coefficients
# ----------------------------------------------------------------------------

print('\n--- Curve fit coefficients from TTC ---')
print('a\tb\tc\talpha\tbeta')
for c in coeffs:
    print(f'{c[0]:.4f}\t{c[1]:.4f}\t{c[2]:.4f}\t{c[3]:.4f}\t{c[4]:.4f}')
print('')

# Print tau, resistor, and capacitor values
# ----------------------------------------------------------------------------

soc = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

print(f"--- RC parameters from TTC ---")
print(f"{'soc [-]':10} {'tau1 [s]':10} {'tau2 [s]':10} {'r0 [Ω]':10} {'r1 [Ω]':10} {'r2 [Ω]':10} {'c1 [F]':10} {'c2 [F]':10}")
for s, r in zip(soc, rctau):
    print(f'{s:<10} {r[0]:<10.2f} {r[1]:<10.2f} {r[2]:<10.4f} {r[3]:<10.4f} {r[4]:<10.4f} {r[5]:<10.1f} {r[6]:<10.1f}')
print('')
