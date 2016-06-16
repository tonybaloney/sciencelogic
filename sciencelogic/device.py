from performance_data import PerformanceData


class Device(object):
    def __init__(self, device_uri, device_description, client, fill_details=False):
        self._client = client
        self.uri = device_uri
        self.description = device_description
        if fill_details:
            self._fill_details()
        else:
            self.details = None

    def __repr__(self):
        return self.description

    def _fill_details(self):
        d = self._client.get(self.uri)
        self.details = d.json()
        
    def performance_counters(self):
        if self.details is None:
            self._fill_details()
        counters=[]
        u = self.details['performance_data']['URI']
        for u_data in self._client.get(u).json()['result_set']:
            counters.append(PerformanceData(self._client, u_data))
        return counters
