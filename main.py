"""
Driver for equivalent circuit model and its components.
"""

import argparse
import utils
import ecmlib


def main(args):

    # Parameters for data file paths and equivalent circuit model
    params = utils.params

    # Print parameters to console
    if args.cmd == 'params' or args.parameters:
        utils.print_parameters(params)

    # Plot the original and processed HPPC battery cell data
    if args.cmd == 'hppcdata':
        orig = ecmlib.HppcData(params.datafiles['hppc'])
        proc = ecmlib.HppcData.process(params.datafiles['hppc'])
        utils.plot_hppc_orig(orig)
        utils.plot_hppc_proc(proc)

    # Plot the original and processed discharge battery cell data
    if args.cmd == 'disdata':
        if args.dis == '1c':
            orig = ecmlib.DischargeData(params.datafiles['bitrode_1c'])
            proc = ecmlib.DischargeData.process(params.datafiles['bitrode_1c'])
        if args.dis == '2c':
            orig = ecmlib.DischargeData(params.datafiles['bitrode_2c'])
            proc = ecmlib.DischargeData.process(params.datafiles['bitrode_2c'])
        if args.dis == '3c':
            orig = ecmlib.DischargeData(params.datafiles['bitrode_3c'])
            proc = ecmlib.DischargeData.process(params.datafiles['bitrode_3c'])
        utils.plot_discharge_orig(orig)
        utils.plot_discharge_proc(proc)

    # Plot the original and processed temperature data associated with the discharge battery cell data
    if args.cmd == 'tempdata':
        if args.dis == '1c':
            dis = ecmlib.DischargeData.process(params.datafiles['bitrode_1c'])
            orig = ecmlib.TemperatureData(params.datafiles['temp_1c'], dis.ti, dis.tf)
            proc = ecmlib.TemperatureData.process(params.datafiles['temp_1c'], dis.ti, dis.tf)
        if args.dis == '2c':
            dis = ecmlib.DischargeData.process(params.datafiles['bitrode_2c'])
            orig = ecmlib.TemperatureData(params.datafiles['temp_2c'], dis.ti, dis.tf)
            proc = ecmlib.TemperatureData.process(params.datafiles['temp_2c'], dis.ti, dis.tf)
        if args.dis == '3c':
            dis = ecmlib.DischargeData.process(params.datafiles['bitrode_3c'])
            orig = ecmlib.TemperatureData(params.datafiles['temp_3c'], dis.ti, dis.tf)
            proc = ecmlib.TemperatureData.process(params.datafiles['temp_3c'], dis.ti, dis.tf)
        utils.plot_temp_orig(orig)
        utils.plot_temp_proc(proc)

    # Print and plot SOC and OCV values as determined from the HPPC data
    if args.cmd == 'soc':
        hppc_proc = ecmlib.HppcData.process(params.datafiles['hppc'])
        ecm = ecmlib.EquivCircModel(hppc_proc, params)
        utils.print_soc_ocv(ecm)
        utils.plot_soc_ocv(hppc_proc, ecm)

    # Print and plot curve fit of HPPC data
    if args.cmd == 'curvefit':
        hppc_proc = ecmlib.HppcData.process(params.datafiles['hppc'])
        ecm = ecmlib.EquivCircModel(hppc_proc, params)
        utils.print_coeffs(ecm)
        utils.plot_curve_fit(hppc_proc, ecm)

    # Print resistor and capacitor values for each SOC section in the HPPC data
    if args.cmd == 'rctau':
        hppc_proc = ecmlib.HppcData.process(params.datafiles['hppc'])
        ecm = ecmlib.EquivCircModel(hppc_proc, params)
        utils.print_rctau(ecm)

    # Plot and compare ECM to the HPPC battery cell data
    if args.cmd == 'ecm':
        hppc_proc = ecmlib.HppcData.process(params.datafiles['hppc'])
        ecm = ecmlib.EquivCircModel(hppc_proc, params)
        coeffs_ttc = ecm.curve_fit_coeff(ecm.func_ttc, 5)
        rctau = ecm.rctau_ttc(coeffs_ttc)
        v_ecm = ecm.v_ecm(ecm.soc, ecm.ocv, rctau)
        utils.plot_v_ecm(hppc_proc, v_ecm)

    # Plot and compare ECM to discharge data and associated temperature data
    if args.cmd == 'temp':
        if args.dis == '1c':
            dis = ecmlib.DischargeData.process(params.datafiles['bitrode_1c'])
            proc = ecmlib.TemperatureData.process(params.datafiles['temp_1c'], dis.ti, dis.tf)
        if args.dis == '2c':
            dis = ecmlib.DischargeData.process(params.datafiles['bitrode_2c'])
            proc = ecmlib.TemperatureData.process(params.datafiles['temp_2c'], dis.ti, dis.tf)
        if args.dis == '3c':
            dis = ecmlib.DischargeData.process(params.datafiles['bitrode_3c'])
            proc = ecmlib.TemperatureData.process(params.datafiles['temp_3c'], dis.ti, dis.tf)
        utils.plot_discharge_proc(dis)
        utils.plot_temp_proc(proc)

    utils.show_plots()


if __name__ == '__main__':

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd',
                        choices=['params', 'hppcdata', 'disdata', 'tempdata', 'soc', 'curvefit', 'rctau', 'ecm', 'temp'],
                        help='run equivalent circuit model or its components')
    parser.add_argument('dis',
                        nargs='?',
                        choices=['1c', '2c', '3c'],
                        help='rate of discharge for data')
    parser.add_argument('-p', '--parameters', action='store_true', help='print parameters')
    args = parser.parse_args()

    if args.cmd == 'disdata' and not args.dis:
        parser.error('dis arguments as 1c, 2c, or 3c is required')

    if args.cmd == 'tempdata' and not args.dis:
        parser.error('dis arguments as 1c, 2c, or 3c is required')

    if args.cmd == 'temp' and not args.dis:
        parser.error('dis arguments as 1c, 2c, or 3c is required')

    main(args)
