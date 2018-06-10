from sciencelogic.client import Client
import matplotlib.pyplot as plt
#import json
import pprint
from argparse import ArgumentParser

options = ArgumentParser(description="A simple program to SNMP query a device.")
options.add_argument("url",
                     help="The host URL.")
options.add_argument("Userid",
                     help="The Username to use.")
options.add_argument("password",
                     help="The password.")
args = options.parse_args()
c = Client(args.Userid, args.password, args.url)

# API details
# print("sysinfo:", c.sysinfo)
print("Sysinfo:")
pprint.pprint(c.sysinfo)

print("Device Info:")
# devices = c.get_device(449)  # BXB DCC GW.
devices = c.get_device(449)  # BXB DCC GW.
print(devices)

# Get the first device
# devices = c.devices(details=False, options=["filter.name=bxb23-dmzbb-gw1.cisco.com"])
devices = c.devices(details=True, options=["filter.name.contains=ntp"])
print("Device details:")
for d in devices:
    # print("device details:", d.details)
    pprint.pprint(d.details)

# Get a list of available performance counters
counters = d.performance_counters()

print("Available counters")
for counter in counters:
    print("{}".format(counter.name()))

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
