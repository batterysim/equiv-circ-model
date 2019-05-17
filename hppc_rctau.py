"""
RC parameters determined from the HPPC battery cell data.
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
coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
rctau = ecm.rctau_ttc(coeffs)

# Print results
# ----------------------------------------------------------------------------

utils.print_parameters(params)
utils.print_rctau(rctau)
