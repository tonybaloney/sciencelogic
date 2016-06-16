from sciencelogic.client import Client
import time
import matplotlib.pyplot as plt


c = Client('jazz', 'hands!', 'https://au-monitoring.mcp-services.net/')
print(c.sysinfo)
print(c.devices())

d1 = c.devices()[0]

d1._fill_details()

print(d1.details)

counters = d1.performance_counters()
print(counters)

data = counters[0].get_data()

print(data)

keys = []
values = []



for key, value in data.iteritems():
    keys.append(key)
    values.append(value)

plt.plot(keys, values, 'ro')
plt.ylabel(counters[0].__repr__())
plt.show()