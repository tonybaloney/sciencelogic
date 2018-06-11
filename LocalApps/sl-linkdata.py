from sciencelogic.client import Client
import pandas as pd
# import matplotlib.pyplot as plt
import json
# import pprint
from argparse import ArgumentParser
import yaml


returned_columns = ['time', 'device', 'interface', 'interface_speed',
                    'sample_type', 'd_octets_in', 'd_octets_out']


def get_host_data(connection:Client, hostname:str, host_info:dict) -> pd.DataFrame:
    """
    Given a dictionary defining the host info to get, and a connection to the
    ScienceLogic collector, fetch the data info a dataframe.

    :param connection:
    :param hostname:
    :param host_info:
    :return:
    """
    # noinspection PyTypeChecker
    devices = connection.devices(details=True, options=["filter.name.contains={}".format(hostname)])
    host_data = []
    for device in devices:  # There should only be one...
        # print(">", device)
        interface_response = connection.get(device.details['interfaces']['URI'])
        interface_list = json.loads(interface_response.text)
        for interface_reference in interface_list['result_set']:
            # print(interface_reference['description'], "=?=", host_info["interfaces"])
            if interface_reference['description'] in host_info["interfaces"]:
                print(">>", device, interface_reference['description'])
                # pprint.pprint(int_ref)

                interface_detail = connection.get(interface_reference['URI'])
                interface = json.loads(interface_detail.text)
                # print(">>>", interface['alias'], "/", interface['measure'])
                interface_description = interface_reference['description']
                # pprint.pprint(interface)

                if 'normalized_hourly' in interface['interface_data']:
                    temp_performance_data = json.loads(
                        connection.get(interface['interface_data']['normalized_hourly']['URI']).text)
                elif 'data' in interface['interface_data']:
                    temp_performance_data = json.loads(
                        connection.get(interface['interface_data']['data']['URI']).text)
                else:
                    temp_performance_data = []

                if temp_performance_data:
                    poll_rate = int(interface['poll_rate']) * 60
                    for performance_type in ["min", "max", "avg"]:
                        # noinspection PyTypeChecker
                        interface_performance_data = pd.DataFrame(data={
                            'time': [pd.to_datetime(timestamp, unit='s') for timestamp in temp_performance_data['data']['d_octets_in'][performance_type]],
                            'd_octets_in': [float(temp_performance_data['data']['d_octets_in'][performance_type][data_point]) / poll_rate
                                            for data_point in temp_performance_data['data']['d_octets_in'][performance_type]],
                            'd_octets_out': [float(temp_performance_data['data']['d_octets_out'][performance_type][data_point]) / poll_rate
                                             for data_point in temp_performance_data['data']['d_octets_out'][performance_type]],
                        })
                        interface_performance_data["sample_type"] = performance_type
                        if 'ifHighSpeed' in interface:
                            interface_performance_data["interface_speed"] = int(interface['ifHighSpeed']) * 1000000
                        else:
                            int(interface['ifSpeed'])
                        interface_performance_data["device"] = hostname
                        interface_performance_data["interface"] = interface_description
                        host_data.append(interface_performance_data)

    if host_data:
        return pd.concat(host_data)
    else:
        return pd.DataFrame(data=[], columns=returned_columns)


def get_data_from_collector(collector_info:dict, userid:str, password:str) -> pd.DataFrame:
    """
    Given a dictionary defining the ScienceLogic collector and the hosts/interfaces
    to collect data for, get the data and return it in a data frame.

    :param collector_info:
    :param userid:
    :param password:
    """
    all_host_data = None
    for sl_collector in collector_info:  # There should only be one...
        collector_url = collector_info[sl_collector]['url']
        connection = Client(userid, password, collector_url)
        for device_info in collector_info[sl_collector]['hosts']:
            for hostname in device_info:
                print(">", hostname)
                host_data = get_host_data(connection, hostname, device_info[hostname])
                if all_host_data is None:
                    all_host_data = host_data
                else:
                    all_host_data = pd.concat([all_host_data, host_data])
    return all_host_data


def process_cmd_line():
    """
    Process the args and do the work.
    :return:
    """
    options = ArgumentParser(description="A program to get MTV5 intersite link utilization from SciLo.")
    options.add_argument("userid",
                         help="The Username to use.")
    options.add_argument("password",
                         help="The password.")
    options.add_argument("cfgfile",
                         help="The YAML file defining the data to collect.")
    options.add_argument("outfile",
                         help="The file to write to",)
    options.add_argument("-c", "--create",
                         action="store_true",
                         help="Create the file, even if it exists.")
    options.add_argument("-n", "--names",
                         action="store_true",
                         help="Write the column names (header row)")
    type_group = options.add_mutually_exclusive_group(required=False)
    type_group.add_argument("--avg",
                            action="store_true",
                            help="Save average rate data (default)")
    type_group.add_argument("--min",
                            action="store_true",
                            help="Save minimum rate data")
    type_group.add_argument("--max",
                            action="store_true",
                            help="Save maximum rate data")
    args = options.parse_args()

    if args.create:
        filemode = "w"
    else:
        filemode = "a"

    if args.min:
        stat_type = "min"
    elif args.max:
        stat_type = "max"
    else:
        stat_type = "avg"

    try:
        config_file = open(args.cfgfile, "r")
    except IOError:
        print("Config file", args.cfgfile, "doesn't exist - exiting.")
        exit(1)
    device_info = yaml.load(config_file)

    all_host_data = None
    for sl_collector in device_info['collectors']:
        host_data = get_data_from_collector(sl_collector, args.userid, args.password)
        if all_host_data is None:
            all_host_data = host_data
        else:
            all_host_data = pd.concat([all_host_data, host_data])
    all_host_data.loc[:, returned_columns]\
        .to_csv(args.outfile, mode=filemode, index=False, header=args.names)


if __name__ == '__main__':
    process_cmd_line()
