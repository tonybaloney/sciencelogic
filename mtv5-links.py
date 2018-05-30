from sciencelogic.client import Client
import pandas as pd
# import matplotlib.pyplot as plt
import json
# import pprint
from argparse import ArgumentParser


def collect_info(userid, password, hostname, dev_info):
    """
    Log into SciLo at the URL given, and get the device info.

    :param userid:
    :param password:
    :param hostname:
    :param dev_info:
    :return:
    """
    dev_data = {}
    c = Client(userid, password, dev_info["url"])

    # Get the first device
    # noinspection PyTypeChecker
    devices = c.devices(details=True, options=["filter.name.contains={}".format(hostname)])
    # print("Device details for {}:".format(hostname))
    for d in devices:
        dev_data = {
            'hostname': hostname,
            'ints': []
        }
        # print("device details:", d.details)
        # print(">", d.details['ip'])
        # pprint.pprint(d.details)

        int_resp = c.get(d.details['interfaces']['URI'])
        int_list = json.loads(int_resp.text)
        for int_ref in int_list['result_set']:
            int_perf_data = {}
            if int_ref['description'] in dev_info["ints"]:
                # print(">>")
                # pprint.pprint(int_ref)

                int_detail = c.get(int_ref['URI'])
                interface = json.loads(int_detail.text)
                # print(">>>", interface['alias'], "/", interface['measure'])
                int_perf_data['int'] = int_ref['description']
                # pprint.pprint(interface)

                if 'normalized_hourly' in interface['interface_data']:
                    temp_perf_data = json.loads(
                        c.get(interface['interface_data']['normalized_hourly']['URI']).text)
                elif 'data' in interface['interface_data']:
                    temp_perf_data = json.loads(
                        c.get(interface['interface_data']['data']['URI']).text)
                else:
                    temp_perf_data = []

                if temp_perf_data:
                    int_perf_data['ints'] = {}
                    for y in ["min", "max", "avg"]:
                        # noinspection PyTypeChecker
                        int_perf_data[y] = pd.DataFrame(data={
                            'time': [pd.to_datetime(x, unit='s') for x in temp_perf_data['data']['d_octets_in'][y]],
                            'd_octets_in': [temp_perf_data['data']['d_octets_in'][y][x]
                                            for x in temp_perf_data['data']['d_octets_in'][y]],
                            'd_octets_out': [temp_perf_data['data']['d_octets_out'][y][x]
                                             for x in temp_perf_data['data']['d_octets_out'][y]],
                        })
                        int_perf_data[y]["device"] = hostname + ":" + int_ref["description"]
                dev_data['ints'].append(int_perf_data)

    return dev_data


def process_cmd_line():
    """
    Process the args and do the work.
    :return:
    """
    options = ArgumentParser(description="A program to get MTV5 intersite link utilization from SciLo.")
    options.add_argument("Userid",
                         help="The Username to use.")
    options.add_argument("password",
                         help="The password.")
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
    type_group.add_argument("-a", "--max",
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

    device_info = {
        "sjc12-rbb-gw4": {
            "url": "https://central2.cisco.com",
            "ints": ["Te2/14", "Te5/14"],
            "SwapDirection": False
        },
        "mtv5-mda2-sbb-gw2": {
            "url": "https://west2.cisco.com",
            "ints": ["Te6/16", "Te7/5"],
            "SwapDirection": True
        }
    }

    for cur_device in device_info:
        device_info[cur_device]['PerfData'] = collect_info(args.Userid, args.password,
                                                           cur_device, device_info[cur_device])['ints']

    df_list = []
    host_list = [device_info[host]['PerfData'] for host in device_info]
    for int_list in host_list:
        for int_data in int_list:
            # noinspection PyTypeChecker
            df_list.append(int_data[stat_type])
    df = pd.concat(df_list)
    df.to_csv(args.outfile, mode=filemode, index=False, header=args.names)

    # print("Exiting")


if __name__ == '__main__':
    process_cmd_line()
