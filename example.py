from sciencelogic.client import Client
import time
import matplotlib.pyplot as plt


c = Client('jazz', 'hands!', 'https://au-monitoring.mcp-services.net/')

# API details
print(c.sysinfo)

# Get the first device
d1 = c.devices()[0]

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