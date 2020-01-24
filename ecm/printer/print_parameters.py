import textwrap


def print_parameters(pm):
    """
    Print parameters to console.
    """
    params_string = f"""
    === Data Files ===

    {'hppc':15} {pm.datafiles['cell_hppc']:>12}
    {'bitrode_1c':15} {pm.datafiles['cell_discharge_1c']:>12}

    === Cell Parameters ===

    {'a_surf':10} {pm.a_surf:>12}  {'m²':<10} surface area
    {'cp_cell':10} {pm.cp_cell:>12}  {'J/(kg K)':<10} heat capacity of battery cell
    {'eta_chg':10} {pm.eta_chg:>12}  {'-':<10} coulombic charge efficiency for cell
    {'eta_dis':10} {pm.eta_dis:>12}  {'-':<10} coulombic discharge efficiency for cell
    {'h_conv':10} {pm.h_conv:>12}  {'W/(m² K)':<10} convective heat transfer coefficient
    {'m_cell':10} {pm.m_cell:>12}  {'kg':<10} mass of battery cell
    {'q_cell':10} {pm.q_cell:>12}  {'Ah':<10} total battery cell capacity
    {'tinf':10} {pm.tinf:>12}  {'K':<10} ambient temperature
    """
    params_dedent = textwrap.dedent(params_string)
    print(params_dedent)
