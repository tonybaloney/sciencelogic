from presentations import Presentation


class PerformanceData(object):
    def __init__(self, client, options):
        self._client = client
        self.options = options
    
    def name(self):
        return self.options['appname']
    
    def __repr__(self):
        return "%s" % (self.name())
    
    def get_presentations(self):
        return [Presentation(p, self._client) for p in self.options['presentations']]
    
    def get_presentation_data(self, presentation):
        return presentation.get_data()
