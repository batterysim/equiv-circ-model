import params
import plotter

from discharge_data import DischargeData
from temperature_data import TemperatureData


def view_discharge_data():
    """
    View plots of the discharge data and associated temperatures.
    """

    dis1c = DischargeData(params.datafiles['bitrode_1c'])
    dis2c = DischargeData(params.datafiles['bitrode_2c'])
    dis3c = DischargeData(params.datafiles['bitrode_3c'])

    f1c = params.datafiles['temp_1c']
    f2c = params.datafiles['temp_2c']
    f3c = params.datafiles['temp_3c']
    temp1c = TemperatureData(f1c, dis1c.ti, dis1c.tf)
    temp2c = TemperatureData(f2c, dis2c.ti, dis2c.tf)
    temp3c = TemperatureData(f3c, dis3c.ti, dis3c.tf)

    # Process current, voltage, and temperature data for one section of the original data.
    dis_1c = DischargeData.process(params.datafiles['bitrode_1c'])
    dis_2c = DischargeData.process(params.datafiles['bitrode_2c'])
    dis_3c = DischargeData.process(params.datafiles['bitrode_3c'])

    temp_1c = TemperatureData.process(f1c, dis_1c.ti, dis_1c.tf)
    temp_2c = TemperatureData.process(f2c, dis_2c.ti, dis_2c.tf)
    temp_3c = TemperatureData(f3c, dis_3c.ti, dis_3c.tf)

    # Process current, voltage, and temperature data for just the discharge portion.
    dis_only_1c = DischargeData.process_discharge_only(params.datafiles['bitrode_1c'])
    dis_only_2c = DischargeData.process_discharge_only(params.datafiles['bitrode_2c'])
    dis_only_3c = DischargeData.process_discharge_only(params.datafiles['bitrode_3c'])

    temp_only_1c = TemperatureData.process(f1c, dis_only_1c.ti, dis_only_1c.tf)
    temp_only_2c = TemperatureData.process(f2c, dis_only_2c.ti, dis_only_2c.tf)
    temp_only_3c = TemperatureData.process(f3c, dis_3c.ti, dis_3c.tf)

    # Create plot figures and show plots
    plotter.plot_orig_dis_electric_data(dis1c, dis2c, dis3c)
    plotter.plot_orig_dis_temps_data(temp1c, temp2c, temp3c)
    plotter.plot_dis_electric_data(dis_1c, dis_2c, dis_3c, dis_only_1c, dis_only_2c, dis_only_3c)
    plotter.plot_dis_temps_data(temp_1c, temp_2c, temp_3c, temp_only_1c, temp_only_2c, temp_only_3c)
    plotter.show_plots()
