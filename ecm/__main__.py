import argparse
import logging
import driver


def main():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-vd', '--viewcelldis', action='store_true', help='view battery cell discharge data')
    parser.add_argument('-vh', '--viewcellhppc', action='store_true', help='view battery cell HPPC data')
    parser.add_argument('-vm', '--viewmodulehppc', action='store_true', help='view battery module HPPC data')
    parser.add_argument('-rf', '--runcellfit', action='store_true', help='run curve fit of battery cell HPPC data')
    parser.add_argument('-rc', '--runcellrctau', action='store_true', help='run RC parameters for battery cell HPPC data')
    parser.add_argument('-rs', '--runcellsococv', action='store_true', help='run SOC and OCV for battery cell HPPC data')
    parser.add_argument('-re', '--runcellecm', action='store_true', help='run ECM for battery cell and compare to HPPC data')
    parser.add_argument('-rd', '--runpackdis', action='store_true', help='run ECM for battery pack at constant discharge')
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.info('Start equivalent circuit model...')

    # Handle command line arguments
    if args.viewcelldis:
        logging.info('View battery cell discharge and temperature data...')
        driver.view_cell_discharge_data()

    elif args.viewcellhppc:
        logging.info('View battery cell HPPC data...')
        driver.view_cell_hppc_data()

    elif args.viewmodulehppc:
        logging.info('View battery module HPPC data...')
        driver.view_module_hppc_data()

    elif args.runcellfit:
        logging.info('Run curve fit of the battery cell HPPC data...')
        driver.run_cell_hppc_curvefit()

    elif args.runcellrctau:
        logging.info('Run RC parameters for the battery cell HPPC data...')
        driver.run_cell_hppc_rctau()

    elif args.runcellsococv:
        logging.info('Run SOC and OCV for the battery cell HPPC data...')
        driver.run_cell_hppc_sococv()

    elif args.runcellecm:
        logging.info('Run ECM for battery cell and compare to HPPC data...')
        driver.run_cell_ecm_hppc()

    elif args.runpackdis:
        logging.info('Run ECM for battery pack at constant discharge...')
        driver.run_pack_ecm_discharge()

    # Log message if there is no input arguments
    else:
        logging.info('No input argument. Please provide an input argument...')

    # Program has completed execution
    logging.info('Done.')


if __name__ == '__main__':
    main()
