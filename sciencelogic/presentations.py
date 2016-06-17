class Presentation(object):
    def __init__(self, presentation_dict, client):
        """
        Instantiate a new presentation of a performance counter

        :param presentation_dict: The presentation configuration data
        :type  presentation_dict: ``dict``
        """
        self.name = presentation_dict['presname']
        self.data_uri = presentation_dict['data']['URI']
        self._client = client

    def get_data(self):
        """
        Get the data for this presentation

        :rtype: ``dict``
        """
        r = self._client.get(self.data_uri)
        return r.json()['data'].get('0', {})
