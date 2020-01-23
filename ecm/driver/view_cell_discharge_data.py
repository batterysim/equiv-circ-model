import params
import plotter

from cell_discharge_data import CellDischargeData
from cell_temperature_data import CellTemperatureData


def view_cell_discharge_data():
    """
    View plots of the battery cell discharge data and associated temperatures.
    """

    dis1c = CellDischargeData(params.datafiles['bitrode_1c'])
    dis2c = CellDischargeData(params.datafiles['bitrode_2c'])
    dis3c = CellDischargeData(params.datafiles['bitrode_3c'])

    f1c = params.datafiles['temp_1c']
    f2c = params.datafiles['temp_2c']
    f3c = params.datafiles['temp_3c']
    temp1c = CellTemperatureData(f1c, dis1c.ti, dis1c.tf)
    temp2c = CellTemperatureData(f2c, dis2c.ti, dis2c.tf)
    temp3c = CellTemperatureData(f3c, dis3c.ti, dis3c.tf)

    # Process current, voltage, and temperature data for one section of the original data.
    dis_1c = CellDischargeData.process(params.datafiles['bitrode_1c'])
    dis_2c = CellDischargeData.process(params.datafiles['bitrode_2c'])
    dis_3c = CellDischargeData.process(params.datafiles['bitrode_3c'])

    temp_1c = CellTemperatureData.process(f1c, dis_1c.ti, dis_1c.tf)
    temp_2c = CellTemperatureData.process(f2c, dis_2c.ti, dis_2c.tf)
    temp_3c = CellTemperatureData(f3c, dis_3c.ti, dis_3c.tf)

    # Process current, voltage, and temperature data for just the discharge portion.
    dis_only_1c = CellDischargeData.process_discharge_only(params.datafiles['bitrode_1c'])
    dis_only_2c = CellDischargeData.process_discharge_only(params.datafiles['bitrode_2c'])
    dis_only_3c = CellDischargeData.process_discharge_only(params.datafiles['bitrode_3c'])

    temp_only_1c = CellTemperatureData.process(f1c, dis_only_1c.ti, dis_only_1c.tf)
    temp_only_2c = CellTemperatureData.process(f2c, dis_only_2c.ti, dis_only_2c.tf)
    temp_only_3c = CellTemperatureData.process(f3c, dis_3c.ti, dis_3c.tf)

    # Create plot figures and show plots
    plotter.plot_orig_dis_electric_data(dis1c, dis2c, dis3c)
    plotter.plot_orig_dis_temps_data(temp1c, temp2c, temp3c)
    plotter.plot_dis_electric_data(dis_1c, dis_2c, dis_3c, dis_only_1c, dis_only_2c, dis_only_3c)
    plotter.plot_dis_temps_data(temp_1c, temp_2c, temp_3c, temp_only_1c, temp_only_2c, temp_only_3c)
    plotter.show_plots()
