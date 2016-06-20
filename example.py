from sciencelogic.client import Client
import matplotlib.pyplot as plt


c = Client('jazz', 'hands!', 'https://au-monitoring.mcp-services.net/')

# API details
print(c.sysinfo)

# Get the first device
devices = c.devices(details=True)

for d in devices:
    print(d.details)

# Custom attribute
target_server_id = '56a20d29-95cc-46b8-b43c-41a96be18ace'

# Match by custom attribute
d1 = [device for device in devices
      if device.details['c-server-id'] == target_server_id][0]

# Get the details of the client
print(d1.details)

# Get a list of available performance counters
counters = d1.performance_counters()

print ("Available counters")
for counter in counters:
    print("%s" % (counter.name()))

# Get historic performance data of the first counter
data = counters[0].get_presentations()[0].get_data()

# Graph the data in matplotlib
keys = []
values = []
for key, value in data.iteritems():
    keys.append(key)
    values.append(value)

plt.plot(keys, values, 'ro')
plt.ylabel(counters[0].__repr__())
plt.show()
