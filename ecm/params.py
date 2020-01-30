"""
Parameters for the 2013 Nissan Leaf battery cell, battery module, and
associated data files.

Note: Rated capacity of cell is stated as 33.1 Ah. According to Hsin's email,
use 32-33 Ah for HPPC tests. According to Hsin's email, use 30.6 Ah for the
discharge tests.
"""

# Surface area of the battery cell [m²]
a_surf = 0.067569

# Heat capacity of the battery cell [J/(kg K)]
# cp_cell = 1100
# cp_cell = 1300
cp_cell = 1600

# Coulombic efficiency of the battery cell for charge and discharge [-]
eta_chg = 0.98
eta_dis = 1.00

# Convective heat transfer coefficient [W/(m² K)]
# h_conv = 10
# h_conv = 12
h_conv = 9.5

# Mass of a single battery cell [kg]
m_cell = 0.799

# Total capacity of the battery cell [Ah]
# q_cell = 32.0
q_cell = 30.6

# Ambient temperature [K]
tinf = 298.15

# Data files for HPPC and discharge tests
datafiles = {
    'cell_discharge_1c': 'data/cell-discharge-bitrode-1c.csv',
    'cell_discharge_2c': 'data/cell-discharge-bitrode-2c.csv',
    'cell_discharge_3c': 'data/cell-discharge-bitrode-3c.csv',
    'cell_temperature_1c': 'data/cell-discharge-temperature-1c.lvm',
    'cell_temperature_2c': 'data/cell-discharge-temperature-2c.lvm',
    'cell_temperature_3c': 'data/cell-discharge-temperature-3c.lvm',
    'cell_hppc': 'data/cell-low-current-hppc-25c-2.csv',
    'module1_hppc_23deg': 'data/module1-electchar-65ah-23deg.csv',
    'module1_hppc_45deg': 'data/module1-electchar-65ah-45deg.csv',
    'module2_hppc_23deg': 'data/module2-electchar-65ah-23deg.csv',
    'module2_hppc_45deg': 'data/module2-electchar-65ah-45deg.csv',
    'module3_hppc_23deg': 'data/module3-electchar-65ah-23deg.csv',
    'module3_hppc_45deg': 'data/module3-electchar-65ah-45deg.csv',
    'module123': 'data/module123-ir-65ah-us06.csv',
}
