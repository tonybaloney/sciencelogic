import pandas as pd
import matplotlib.pyplot as plt
# import json
# import pprint
from argparse import ArgumentParser


data_columns = ['time', 'device', 'interface', 'interface_speed',
                'sample_type', 'd_octets_in', 'd_octets_out']


def generate_plots(data: pd.DataFrame, plot_min: bool = True,
                   plot_avg: bool = True, plot_max: bool = True) -> None:
    """
    Given a dataframe of rate data, plot it.

    :param data: The dataframe of rate date.
    :param plot_min: If True, plot the min rates.
    :param plot_avg: If True, plot the avg rates.
    :param plot_max: If True, plot the max rates.
    :return: None.
    """
    # for device_name in data.device.unique():
    #     device_data = data.loc[data.loc[:, "device"] == device_name, :]
    #     for interface_name in device_data.interface.unique():
    #         interface_data = device_data.loc[device_data.loc[:, "interface"] == interface_name, :]
    for device_name, device_data in data.groupby("device"):
        for interface_name, interface_data in device_data.groupby("interface"):
            print("{}:{}".format(device_name, interface_name))
    pass


def get_rate_data(filename: str) -> pd.DataFrame:
    """
    Read the rate data from the datafile into a dataframe, process it if necessary,
    and return the dataframe.

    :param filename: The file to get the data from.
    :return: A pandas dataframe containing the read data.
    """
    try:
        datafile = open(filename, "r")
        data = pd.read_csv(datafile)
    except IOError as error:
        print("Error: Unable to read {}".format(filename))
        print(error)
        data = pd.DataFrame(data=None, columns=data_columns)

    grouped_data = data.groupby(by=["time", "device", "interface", "sample_type"])
    data_in = data.loc[grouped_data["d_octets_in"].idxmax(), :]\
        .drop("d_octets_out", axis=1)
    data_out = data.loc[grouped_data["d_octets_out"].idxmax(), :]\
        .drop(["d_octets_in", "interface_speed"], axis=1)
    data_merged = pd.merge(data_in, data_out, on=["time", "device", "interface", "sample_type"])

    return(data_merged)


def process_args() -> None:
    """
    Process the command line and call the routines to do the work.

    :return:
    """
    options = ArgumentParser(description="A program to plot link utilization data from SciLo.")
    options.add_argument("datafile",
                         help="The CSV file containing the data to plot.")
    type_group = options.add_mutually_exclusive_group(required=False)
    type_group.add_argument("--avg",
                            action="store_true",
                            help="Plot average rate data (default)")
    type_group.add_argument("--min",
                            action="store_true",
                            help="Plot minimum rate data")
    type_group.add_argument("--max",
                            action="store_true",
                            help="Plot maximum rate data")
    args = options.parse_args()

    if not (args.min or args.avg or args.max):
        # If nothing is specified, include everything.
        args.min = args.avg = args.max = True

    generate_plots(get_rate_data(args.datafile), args.min, args.avg, args.max)


if __name__ == '__main__':
    process_args()
