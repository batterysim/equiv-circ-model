"""
View plots of the battery module HPPC data.
"""

import matplotlib.pyplot as plt

from ecm import ModuleData
from utils import config_ax

# Battery module HPPC data
# ----------------------------------------------------------------------------

file_hppc = 'data/module1-electchar-65ah-45deg.csv'
data = ModuleData(file_hppc)

# Plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(tight_layout=True)
ax.plot(data.time, data.voltage, color='C3')
config_ax(ax, xylabels=('Time [s]', 'Voltage [V]'))

plt.show()
