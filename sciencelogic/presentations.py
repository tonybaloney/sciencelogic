class Presentation(object):
    """
    A presentation of a monitor's data
    """
    def __init__(self, presentation_dict, client):
        """
        Instantiate a new presentation of a performance counter

        :param presentation_dict: The presentation configuration data
        :type  presentation_dict: ``dict``
        """
        self.name = presentation_dict['presname']
        self.data_uri = presentation_dict['data']['URI']
        self._client = client

    def get_data(self,
                 beginstamp=None,
                 endstamp=None,
                 insert_nulls=1,
                 fetch_indexes=0,
                 duration=None,
                 idx_list=None,
                 idx_max=None,
                 hide_options=1):
        """
        Get the data for this presentation

        :param beginstamp: timestamp for the beginning of the desired range of
            data
        :type  beginstamp: ``str``

        :param endstamp: timestamp for the end of the desired range of data
        :type  endstamp: ``str``

        :param insert_nulls: insert NULLs for all poll dates within the
            specified date range that do not have polled values
        :type  insert_nulls: ``bool``

        :param fetch_indexes: fetch the list of collection indexes (and their
            string labels, if any exist) for the date range instead of
            actual data.
        :type  fetch_indexes: ``bool``

        :param duration: human readable short-hand, such as 24h, 5d,
            90m where h=HOUR, d=DAY, m=MINUTE. Used to specify the amount
            of data to fetch
        :type  duration: ``str``

        :param idx_list: a list of collection indexes for which to fetch data
            (when not specified, all indexes up to idx.max will be fetched)
        :type  idx_list: ``list``

        :param idx_max: limits the maximum number of collection indexes to
            return for the requested presentation data
        :type  idx_max: ``int``

        :param hide_options: hide the available request parameters from the
            response
        :type  hide_options: ``bool``

        :rtype: ``dict``

        .. note:: if fetch_indexes is enabled, idx.max and idx.list will be
            ignored.
        """
        params = {  # defaults
            'insert_nulls': insert_nulls,
            'fetch_indexes': fetch_indexes,
            'hide_options': hide_options,
        }

        if beginstamp:
            params['beginstamp'] = beginstamp

        if endstamp:
            params['endstamp'] = endstamp

        if duration:
            params['duration'] = duration

        if idx_list is not None:
            params['idx.list'] = ','.join(idx_list)

        if idx_max:
            params['idx.max'] = idx_max

        url = self.data_uri
        if beginstamp or endstamp or duration:
            # strip any request params if any timestamps are passed
            url = self.data_uri[:self.data_uri.find('?')]

        data = self._client.get(url, params=params)
        # TODO: '0' is just one of the available collection indices.
        # May be all of them should be returned here?
        return data.json().get('data', {}).get('0', {})
