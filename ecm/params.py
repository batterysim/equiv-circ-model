""""
Parameters for the Nissan Leaf battery cell, battery module, and data files.

Parameters
----------
a_surf : float
    Surface area of battery cell [m²]
cp : float
    Heat capacity of battery cell [J/(kg K)]
h_conv : float
    Convective heat transfer coefficient [W/(m² K)]
eta_chg : float
    Coulombic efficiency of battery cell for charge [-]
eta_dis : float
    Coulombic efficiency of battery cell for discharge [-]
m_cell : float
    Mass of a single battery cell [kg]
q_cell : float
    Total capacity of battery cell [Ah]
tinf : float
    Ambient temperature [K]

Note
----
Rated capacity of cell is stated as 33.1 Ah. According to Hsin's email, use
32-33 Ah for HPPC tests. According to Hsin's email, use 30.6 Ah for the
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

datafiles = {
    'hppc': 'data/NissanLeaf-cell-Low-Current-HPPC-25C-2.csv',
    'bitrode_1c': 'data/1C-Discharge-Bitrode-data.csv',
    'bitrode_2c': 'data/2C-Discharge-Bitrode-data.csv',
    'bitrode_3c': 'data/3C-Discharge-Bitrode-data.csv',
    'temp_1c': 'data/Temperature-1C-discharge.lvm',
    'temp_2c': 'data/Temperature-2C-discharge.lvm',
    'temp_3c': 'data/Temperature-3C-discharge.lvm'
}
