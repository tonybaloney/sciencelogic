class Presentation(object):
    def __init__(self, presentation_dict, client):
        self.name = presentation_dict['presname']
        self.data_uri = presentation_dict['data']['URI']
        self._client = client
        
    def get_data(self):
        r = self._client.get(self.data_uri)
        return r.json()['data']['0']
