import argparse
import logging
import driver


def main():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-vd', '--viewdischarge', action='store_true', help='view discharge data')
    parser.add_argument('-vh', '--viewhppc', action='store_true', help='view HPPC data')
    parser.add_argument('-rf', '--runfit', action='store_true', help='run curve fit of HPPC data')
    parser.add_argument('-rc', '--runrctau', action='store_true', help='run RC parameters for HPPC data')
    parser.add_argument('-rs', '--runsococv', action='store_true', help='run RC parameters for HPPC data')
    parser.add_argument('-rh', '--runhppc', action='store_true', help='run cell ECM and compare to HPPC data')
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.info('Start equivalent circuit model (ECM) program')

    # View plots of the discharge data and associated temperatures
    if args.viewdischarge:
        logging.info('View discharge data')
        driver.view_discharge_data()

    # View plots of the HPPC data.
    if args.viewhppc:
        logging.info('View HPPC data')
        driver.view_hppc_data()

    # Run curve fit of the HPPC battery cell data
    if args.runfit:
        logging.info('Run curve fit of the HPPC battery cell data')
        driver.run_hppc_curvefit()

    # Run RC parameters for the HPPC battery cell data
    if args.runrctau:
        logging.info('Run RC parameters for the HPPC battery cell data')
        driver.run_hppc_rctau()

    # Run state of charge (SOC) and open circuit voltage (OCV) from HPPC data
    if args.runsococv:
        logging.info('Run SOC and OCV from HPPC battery cell data')
        driver.run_hppc_sococv()

    # Run a single cell ECM and compare to HPPC data
    if args.runhppc:
        logging.info('Run single cell ECM and compare to HPPC battery cell data')
        driver.run_hppc_cell()

    # Program has successfully run
    logging.info('Done')


if __name__ == '__main__':
    main()
