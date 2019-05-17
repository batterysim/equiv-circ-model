"""
State of charge (SOC) and open circuit voltage (OCV) from HPPC data.
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

# Open circuit voltage (OCV)
# ----------------------------------------------------------------------------

ocv = ecmlib.ocv(v_pts, z_pts, soc)

# Print and plot results
# ----------------------------------------------------------------------------

utils.print_parameters(params)
utils.print_soc_ocv(v_pts, z_pts)

utils.plot_soc_ocv(data, ocv, soc, i_pts, t_pts, v_pts, z_pts)
utils.show_plots()
