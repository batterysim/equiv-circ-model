"""
View original and processed discharge data from battery cell test.
"""

import utils
import ecmlib

# Parameters for battery cell
# ----------------------------------------------------------------------------

params = utils.params

file_bit = params.datafiles['bitrode_1c']
# file = params.datafiles['bitrode_2c']
# file = params.datafiles['bitrode_3c']

file_temp = params.datafiles['temp_1c']
# file_temp = params.datafiles['temp_2c']
# file_temp = params.datafiles['temp_3c']

# Original and processed discharge battery cell data
# ----------------------------------------------------------------------------

data_orig = ecmlib.DischargeData(file_bit)
data_proc = ecmlib.DischargeData.process(file_bit)

ti = data_proc.ti
tf = data_proc.tf
temp_orig = ecmlib.TemperatureData(file_temp, ti, tf)
temp_proc = ecmlib.TemperatureData.process(file_temp, ti, tf)

# Plot results
# ----------------------------------------------------------------------------

utils.plot_discharge_orig(data_orig)
utils.plot_discharge_proc(data_proc)

utils.plot_temp_orig(temp_orig)
utils.plot_temp_proc(temp_proc)

utils.show_plots()
