"""
Estimate HPPC battery cell voltage using equivalent circuit model (ECM).
"""

import utils
import ecmlib

# Parameters for battery cell
# ----------------------------------------------------------------------------

params = utils.params

eta_chg = params.eta_chg
eta_dis = params.eta_dis
q_cell = params.q_cell
file = params.datafiles['hppc']

# HPPC data
# ----------------------------------------------------------------------------

data = ecmlib.HppcData.process(file)
curr = data.current
time = data.time

# State of charge (SOC)
# ----------------------------------------------------------------------------

soc = ecmlib.soc(curr, time, eta_chg, eta_dis, q_cell)

# Equivalent circuit model (ECM) developed from HPPC data
# ----------------------------------------------------------------------------

ecm = ecmlib.HppcEcm(data)

i_pts, t_pts, v_pts, z_pts = ecm.points(soc)
coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Open circuit voltage (OCV)
# ----------------------------------------------------------------------------

ocv = ecmlib.ocv(v_pts, z_pts, soc)

# Estimate battery cell voltage for HPPC test
# ----------------------------------------------------------------------------

v_batt = ecmlib.v_ecm(curr, time, soc, ocv, rctau)

# Plot results
# ----------------------------------------------------------------------------

utils.plot_v_ecm(data, v_batt)
utils.show_plots()
