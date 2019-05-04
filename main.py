"""
Driver for equivalent circuit model and its components.
"""

import argparse
import utils
import ecmlib


def main(args):

    # Parameters for data file paths and equivalent circuit model
    params = utils.params

    # Battery data and processed HPPC data
    batt_data = ecmlib.BatteryData(params.datafiles['hppc'])
    hppc_data = ecmlib.HppcData(params.datafiles['hppc'])

    # Equivalent circuit model
    ecm = ecmlib.EquivCircModel(hppc_data, params)
    coeffs_ttc = ecm.curve_fit_coeff(ecm.func_ttc, 5)
    rctau = ecm.rctau_ttc(coeffs_ttc)
    v_ecm = ecm.v_ecm(ecm.soc, ecm.ocv, rctau)

    # Handle command line arguments
    if args.parameters or (args.cmd == 'params'):
        utils.print_parameters(params)
    elif args.cmd == 'battdata':
        utils.plot_data(batt_data)
    elif args.cmd == 'hppcdata':
        utils.plot_data(hppc_data)
    elif args.cmd == 'soc':
        utils.print_soc_ocv(ecm)
        utils.plot_soc_ocv(hppc_data, ecm)
    elif args.cmd == 'curvefit':
        utils.print_coeffs(ecm)
        utils.plot_curve_fit(hppc_data, ecm)
    elif args.cmd == 'rctau':
        utils.print_rctau(ecm)
    elif args.cmd == 'ecm':
        utils.plot_v_ecm(hppc_data, v_ecm)
    else:
        print('Command not available.')


if __name__ == '__main__':

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd',
                        choices=['params', 'battdata', 'hppcdata', 'soc', 'curvefit', 'rctau', 'ecm'],
                        help='run equivalent circuit model or its components')
    parser.add_argument('-p', '--parameters', action='store_true', help='print parameters')
    args = parser.parse_args()

    main(args)
