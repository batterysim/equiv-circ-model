"""
Driver for equivalent circuit model and its components.
"""

import argparse
import utils
import ecmlib


def main(args):

    # Parameters for data file paths and equivalent circuit model
    params = utils.params

    # Handle command line arguments
    if args.cmd == 'params' or args.parameters:
        utils.print_parameters(params)

    if args.cmd == 'hppcdata':
        hppc_data = ecmlib.HppcData(params.datafiles['hppc'])
        utils.plot_hppc_data(hppc_data)

    if args.cmd == 'disdata' and args.dis == '1c':
        data = ecmlib.DischargeData(params.datafiles['bitrode_1c'])
        proc = ecmlib.DischargeData.process(params.datafiles['bitrode_1c'])
        utils.plot_discharge_data(data, proc)

    if args.cmd == 'disdata' and args.dis == '2c':
        data = ecmlib.DischargeData(params.datafiles['bitrode_2c'])
        proc = ecmlib.DischargeData.process(params.datafiles['bitrode_2c'])
        utils.plot_discharge_data(data, proc)

    if args.cmd == 'disdata' and args.dis == '3c':
        data = ecmlib.DischargeData(params.datafiles['bitrode_3c'])
        proc = ecmlib.DischargeData.process(params.datafiles['bitrode_3c'])
        utils.plot_discharge_data(data, proc)

    if args.cmd == 'tempdata' and args.dis == '1c':
        dis = ecmlib.DischargeData.process(params.datafiles['bitrode_1c'])
        data = ecmlib.TemperatureData(params.datafiles['temp_1c'], dis.ti, dis.tf)
        proc = ecmlib.TemperatureData.process(params.datafiles['temp_1c'], dis.ti, dis.tf)
        utils.plot_temp_data(data, proc)

    if args.cmd == 'tempdata' and args.dis == '2c':
        dis = ecmlib.DischargeData.process(params.datafiles['bitrode_2c'])
        data = ecmlib.TemperatureData(params.datafiles['temp_2c'], dis.ti, dis.tf)
        proc = ecmlib.TemperatureData.process(params.datafiles['temp_2c'], dis.ti, dis.tf)
        utils.plot_temp_data(data, proc)

    if args.cmd == 'tempdata' and args.dis == '3c':
        dis = ecmlib.DischargeData.process(params.datafiles['bitrode_3c'])
        data = ecmlib.TemperatureData(params.datafiles['temp_3c'], dis.ti, dis.tf)
        proc = ecmlib.TemperatureData.process(params.datafiles['temp_3c'], dis.ti, dis.tf)
        utils.plot_temp_data(data, proc)

    if args.cmd == 'soc':
        hppc_data = ecmlib.HppcData(params.datafiles['hppc'])
        ecm = ecmlib.EquivCircModel(hppc_data, params)
        utils.print_soc_ocv(ecm)
        utils.plot_soc_ocv(hppc_data, ecm)

    if args.cmd == 'curvefit':
        hppc_data = ecmlib.HppcData(params.datafiles['hppc'])
        ecm = ecmlib.EquivCircModel(hppc_data, params)
        utils.print_coeffs(ecm)
        utils.plot_curve_fit(hppc_data, ecm)

    if args.cmd == 'rctau':
        hppc_data = ecmlib.HppcData(params.datafiles['hppc'])
        ecm = ecmlib.EquivCircModel(hppc_data, params)
        utils.print_rctau(ecm)

    if args.cmd == 'ecm':
        hppc_data = ecmlib.HppcData(params.datafiles['hppc'])
        ecm = ecmlib.EquivCircModel(hppc_data, params)
        coeffs_ttc = ecm.curve_fit_coeff(ecm.func_ttc, 5)
        rctau = ecm.rctau_ttc(coeffs_ttc)
        v_ecm = ecm.v_ecm(ecm.soc, ecm.ocv, rctau)
        utils.plot_v_ecm(hppc_data, v_ecm)


if __name__ == '__main__':

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd',
                        choices=['params', 'hppcdata', 'disdata', 'tempdata', 'soc', 'curvefit', 'rctau', 'ecm'],
                        help='run equivalent circuit model or its components')
    parser.add_argument('dis',
                        nargs='?',
                        choices=['1c', '2c', '3c'],
                        help='rate of discharge for data')
    parser.add_argument('-p', '--parameters', action='store_true', help='print parameters')
    args = parser.parse_args()

    main(args)
