"""
Curve fit of the HPPC battery cell data.
"""

import utils
import ecmlib

# Parameters for battery cell
# ----------------------------------------------------------------------------

params = utils.params
file = params.datafiles['hppc']

# HPPC data
# ----------------------------------------------------------------------------

data = ecmlib.HppcData.process(file)

# Equivalent circuit model (ECM) developed from HPPC data
# ----------------------------------------------------------------------------

ecm = ecmlib.HppcEcm(data)

# Print and plot results
# ----------------------------------------------------------------------------

utils.print_parameters(params)
utils.print_coeffs(ecm)

utils.plot_curve_fit(data, ecm)
utils.show_plots()
