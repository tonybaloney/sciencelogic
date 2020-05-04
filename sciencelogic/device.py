from sciencelogic.performance_data import PerformanceData


class Device(object):
    """
    Represents a monitored device
    """

    def __init__(self, device, uri, client,
                 has_details=False, fetch_details=False):
        """
        Instantiate a new Device object

        :param device: A dict from the /api/device request
        :type  device: ``dict``

        :param client: The API client
        :type  client: :class:`Client`

        """
        self._client = client
        self.uri = uri

        if not isinstance(device, dict):
            raise TypeError("Device is not a valid dict")

        if has_details:
            self.description = device['name']
        else:
            self.description = device['description']
        if not has_details and fetch_details:
            self._fill_details()
        else:
            self.details = device

    def __repr__(self):
        return self.description

    def _fill_details(self):
        """
        Get the detailed information about the device
        """
        device = self._client.get(self.uri)
        self.details = device.json()

    def get_logs(self,
                 extended_fetch=0,
                 hide_filter_info=1,
                 link_disp_field=None,
                 limit=1000,
                 offset=None):
        """
        Get logs for this device

        :param extended_fetch: Fetch entire resource if 1 (true), or resource
            link only if 0 (false).
        :type extended_fetch: ``bool``

        :param hide_filter_info: Suppress filterspec and current filter info
        :type hide_filter_info: ``bool``

        :param link_disp_field: When not using extended_fetch, this determines
            which field is used for the "description" of the resource link
        :type link_disp_field: ``list``

        :param limit: Number of records to retrieve
        :type limit: ``int``

        :param offset: Specifies the index of the first returned resource
            within the entire result set
        :type offset: ``int``

        :rtype: ``list`` of ``dict``
        """
        params = {  # defaults
            'extended_fetch': extended_fetch,
            'hide_filter_info': hide_filter_info,
        }
        if link_disp_field is not None:
            params['link_disp_field'] = ','.join(link_disp_field)

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        uri = self.details['logs']['URI']
        uri = uri[:uri.find('?')]
        data = self._client.get(uri, params=params).json()['result_set']
        if extended_fetch:
            return data.values()

        return [self._client.get(item['URI']).json() for item in data]

    def performance_counters(self):
        """
        Get a list of performance counters for this device

        :rtype: ``list`` of :class:`PerformanceData`
        """
        if self.details is None:
            self._fill_details()
        counters = []
        uri = self.details['performance_data']['URI']
        for u_data in self._client.get(uri).json()['result_set']:
            counters.append(PerformanceData(self._client, u_data))
        return counters
