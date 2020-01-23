
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

    print(f"=== Curve Fit Coefficients ===\n")
    print('--- Coefficients from OTC ---')
    print('a\tb\talpha')
    for c in coeffs_otc:
        print(f'{c[0]:.4f}\t{c[1]:.4f}\t{c[2]:.4f}')

    print('\n--- Coefficients from TTC ---')
    print('\na\tb\tc\talpha\tbeta')
    for c in coeffs_ttc:
        print(f'{c[0]:.4f}\t{c[1]:.4f}\t{c[2]:.4f}\t{c[3]:.4f}\t{c[4]:.4f}')
    print('')
