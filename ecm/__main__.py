import argparse

import params
import plotter
import printer
from discharge_data import DischargeData
from temperature_data import TemperatureData
from hppc_data import HppcData
from equiv_circ_model import EquivCircModel


def main():
    """
    Main entry point for the equivalent circuit model program.
    """

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-vd', '--viewdis', action='store_true', help='view discharge data')
    parser.add_argument('-vh', '--viewhppc', action='store_true', help='view hppc data')
    parser.add_argument('-cv', '--curvefit', action='store_true', help='curve fit hppc data')
    parser.add_argument('-rc', '--rctau', action='store_true', help='rc params from hppc data')
    parser.add_argument('-so', '--sococv', action='store_true', help='soc and ocv from hppc data')
    parser.add_argument('-vb', '--vbatt', action='store_true', help='ecm voltage from hppc data')
    args = parser.parse_args()

    # View original and processed discharge data from battery cell test.
    if args.viewdis:
        file_bit = params.datafiles['bitrode_1c']
        # file = params.datafiles['bitrode_2c']
        # file = params.datafiles['bitrode_3c']

        file_temp = params.datafiles['temp_1c']
        # file_temp = params.datafiles['temp_2c']
        # file_temp = params.datafiles['temp_3c']

        data_orig = DischargeData(file_bit)
        data_proc = DischargeData.process(file_bit)

        ti = data_proc.ti
        tf = data_proc.tf
        temp_orig = TemperatureData(file_temp, ti, tf)
        temp_proc = TemperatureData.process(file_temp, ti, tf)

        plotter.plot_discharge_orig(data_orig)
        plotter.plot_discharge_proc(data_proc)
        plotter.plot_temp_orig(temp_orig)
        plotter.plot_temp_proc(temp_proc)
        plotter.show_plots()

    # View original and processed HPPC data from battery cell test.
    if args.viewhppc:
        file = params.datafiles['hppc']
        data_orig = HppcData(file)
        data_proc = HppcData.process(file)

        plotter.plot_hppc_orig(data_orig)
        plotter.plot_hppc_proc(data_proc)
        plotter.show_plots()

    # Curve fit of the HPPC battery cell data
    if args.curvefit:
        file = params.datafiles['hppc']
        data = HppcData.process(file)

        ecm = EquivCircModel(data, params)

        printer.print_parameters(params)
        printer.print_coeffs(ecm)
        plotter.plot_curve_fit(data, ecm)
        plotter.show_plots()

    # RC parameters determined from the HPPC battery cell data.
    if args.rctau:
        file = params.datafiles['hppc']
        data = HppcData.process(file)

        ecm = EquivCircModel(data, params)
        coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
        rctau = ecm.rctau_ttc(coeffs)

        printer.print_parameters(params)
        printer.print_rctau(rctau)

    # State of charge (SOC) and open circuit voltage (OCV) from HPPC data.
    if args.sococv:
        file = params.datafiles['hppc']
        data = HppcData.process(file)

        ecm = EquivCircModel(data, params)
        soc = ecm.soc()
        ocv, i_pts, t_pts, v_pts, z_pts = ecm.ocv(soc, pts=True)

        printer.print_parameters(params)
        printer.print_soc_ocv(v_pts, z_pts)

        plotter.plot_soc_ocv(data, ocv, soc, i_pts, t_pts, v_pts, z_pts)
        plotter.show_plots()

    # Estimate HPPC battery cell voltage using equivalent circuit model (ECM).
    if args.vbatt:
        file = params.datafiles['hppc']
        data = HppcData.process(file)

        ecm = EquivCircModel(data, params)
        soc = ecm.soc()
        ocv = ecm.ocv(soc)

        coeffs = ecm.curve_fit_coeff(ecm.func_ttc, 5)
        rctau = ecm.rctau_ttc(coeffs)
        v_batt = ecm.v_ecm(soc, ocv, rctau)

        plotter.plot_v_ecm(data, v_batt)
        plotter.show_plots()


if __name__ == '__main__':
    main()
