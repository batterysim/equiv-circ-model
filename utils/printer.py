import textwrap


def print_parameters(pm):
    """
    Print parameters to console.
    """
    params_string = f"""
    --- Data Files ---

    {'hppc':15} {pm.datafiles['hppc']:>12}
    {'bitrode_1c':15} {pm.datafiles['bitrode_1c']:>12}

    --- Cell Parameters ---

    {'a_surf':10} {pm.a_surf:>12}  {'m²':<10} surface area
    {'cp':10} {pm.cp:>12}  {'J/(kg K)':<10} heat capacity of battery cell
    {'eta_chg':10} {pm.eta_chg:>12}  {'-':<10} coulombic charge efficiency for cell
    {'eta_dis':10} {pm.eta_dis:>12}  {'-':<10} coulombic discharge efficiency for cell
    {'h_conv':10} {pm.h_conv:>12}  {'W/(m² K)':<10} convective heat transfer coefficient
    {'m_cell':10} {pm.m_cell:>12}  {'kg':<10} mass of battery cell
    {'q_cell':10} {pm.q_cell:>12}  {'Ah':<10} total battery cell capacity
    {'tinf':10} {pm.tinf:>12}  {'K':<10} ambient temperature

    --- Module Parameters ---

    here
    """
    params_dedent = textwrap.dedent(params_string)
    print(params_dedent)


def print_soc_ocv(ecm):
    """
    Print state of charge (SOC) and open circuit voltage (OCV) points.
    """
    _, _, v_pts, soc_pts = ecm.points
    print('\n=== State of Charge (SOC) and Open Circuit Voltage (OCV) ===\n')
    print(f"{'SOC [-]':10} {'OCV [V]':10}")
    for idx, soc in enumerate(soc_pts):
        print(f'{soc:<10.4f} {v_pts[idx]:<10.4f}')


def print_coeffs(ecm):
    """
    Print curve fit coefficients for one time constant (OTC) and two time
    constant (TTC) functions. OTC represents one RC pair and TTC represents two
    RC pairs.
    """
    func_otc = ecm.func_otc
    func_ttc = ecm.func_ttc

    coeffs_otc = ecm.curve_fit_coeff(func_otc, 3)
    coeffs_ttc = ecm.curve_fit_coeff(func_ttc, 5)

    print(f"\n=== Curve Fit Coefficients ===\n")
    print('a\tb\talpha')
    for c in coeffs_otc:
        print(f'{c[0]:.4f}\t{c[1]:.4f}\t{c[2]:.4f}')

    print('\na\tb\tc\talpha\tbeta')
    for c in coeffs_ttc:
        print(f'{c[0]:.4f}\t{c[1]:.4f}\t{c[2]:.4f}\t{c[3]:.4f}\t{c[4]:.4f}')


def print_rctau(ecm):
    """
    Print tau, resistor, and capacitor values (RC parameters) for each SOC
    section in the HPPC data.
    """
    coeffs_ttc = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs_ttc)

    print(f"\n=== RC Parameters ===\n")
    print(f"{'tau1 [s]':10} {'tau2 [s]':10} {'r0 [Ω]':10} {'r1 [Ω]':10} {'r2 [Ω]':10} {'c1 [F]':10} {'c2 [F]':10}")
    for r in rctau:
        print(f'{r[0]:<10.2f} {r[1]:<10.2f} {r[2]:<10.4f} {r[3]:<10.4f} {r[4]:<10.4f} {r[5]:<10.1f} {r[6]:<10.1f}')
