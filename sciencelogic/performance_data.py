class PerformanceData(object):
    def __init__(self, client, options):
        self._client = client
        self.options = options
        
    def __repr__(self):
        return "%s" % (self.options['appname'])
    
    def get_data(self, hours=24):
        d = self._client.get(self.options['presentations'][0]['data']['URI'])
        return d.json()['data']['0']