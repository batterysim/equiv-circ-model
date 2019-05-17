"""
View original and processed HPPC data from battery cell test.
"""

import utils
import ecmlib

# Parameters for battery cell
# ----------------------------------------------------------------------------

params = utils.params
file = params.datafiles['hppc']

# Original and processed HPPC battery cell data
# ----------------------------------------------------------------------------

data_orig = ecmlib.HppcData(file)
data_proc = ecmlib.HppcData.process(file)

# Plot results
# ----------------------------------------------------------------------------

utils.plot_hppc_orig(data_orig)
utils.plot_hppc_proc(data_proc)
utils.show_plots()
