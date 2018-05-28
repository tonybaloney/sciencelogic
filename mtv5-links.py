from sciencelogic.client import Client
import matplotlib.pyplot as plt
import json
import pprint
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
    c = Client(userid, password, dev_info["url"])

    # Get the first device
    devices = c.devices(details=True, options=["filter.name.contains={}".format(hostname)])
    print("Device details for {}:".format(hostname))
    for d in devices:
        # print("device details:", d.details)
        print(">", d.details['ip'])
        # pprint.pprint(d.details)

        int_resp = c.get(d.details['interfaces']['URI'])
        int_list = json.loads(int_resp.text)
        for int_ref in int_list['result_set']:
            if int_ref['description'] in dev_info["ints"]:
                print(">>")
                pprint.pprint(int_ref)

                int_detail = c.get(int_ref['URI'])
                interface = json.loads(int_detail.text)
                print(">>>", interface['alias'])
                # pprint.pprint(interface)

                # # Get a list of available performance counters
                # counters = interface.performance_counters()
                #
                # print("Available counters")
                # for counter in counters:
                #     print("{}".format(counter.name()))
    return()

    # Get historic performance data of the first counter
    data = counters[0].get_presentations()[0].get_data()

    # Graph the data in matplotlib
    keys = []
    values = []
    for key in data:
        keys.append(key)
        values.append(data[key])

    plt.plot(keys, values)
    plt.ylabel(counters[0].__repr__())
    plt.show()

    # Get some logs from the device.
    logs = d.get_logs(extended_fetch=True)
    for msg in logs:
        print("{}".format(msg))


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
    args = options.parse_args()

    device_info = {
        "sjc12-rbb-gw4": {
            "url": "https://central2.cisco.com",
            "ints": ["Te2/14", "Te5/14"]
        },
        "mtv5-mda2-sbb-gw2": {
            "url": "https://west2.cisco.com",
            "ints": ["Te6/16", "Te7/5"]
        }
    }

    for cur_device in device_info:
        collect_info(args.Userid, args.password, cur_device, device_info[cur_device])


if __name__ == '__main__':
    process_cmd_line()
