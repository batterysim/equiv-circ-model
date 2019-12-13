
def print_rctau(rctau):
    """
    Print tau, resistor, and capacitor values (RC parameters) for each SOC
    section in the HPPC data.
    """

    soc = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

    print(f"=== RC Parameters from TTC ===\n")
    print(f"{'soc [-]':10} {'tau1 [s]':10} {'tau2 [s]':10} {'r0 [Ω]':10} {'r1 [Ω]':10} {'r2 [Ω]':10} {'c1 [F]':10} {'c2 [F]':10}")
    for s, r in zip(soc, rctau):
        print(f'{s:<10} {r[0]:<10.2f} {r[1]:<10.2f} {r[2]:<10.4f} {r[3]:<10.4f} {r[4]:<10.4f} {r[5]:<10.1f} {r[6]:<10.1f}')
    print('')
