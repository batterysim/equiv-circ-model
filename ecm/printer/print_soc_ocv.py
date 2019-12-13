
def print_soc_ocv(v_pts, z_pts):
    """
    Print state of charge (SOC) and open circuit voltage (OCV) points.
    """
    print('\n=== State of Charge (SOC) and Open Circuit Voltage (OCV) ===\n')
    print(f"{'SOC [-]':10} {'OCV [V]':10}")
    for idx, soc in enumerate(z_pts):
        print(f'{soc:<10.4f} {v_pts[idx]:<10.4f}')
    print('')
