from sciencelogic.presentations import Presentation


class PerformanceData(object):
    def __init__(self, client, options):
        """
        Instantiate a new performance counter

        :param client: The API client
        :type  client: :class:`Client`
        """
        self._client = client
        self.options = options

    def name(self):
        return self.options['appname']

    def __repr__(self):
        return "%s" % (self.name())

    def get_presentations(self):
        """
        Get a list of presentations for this performance counter

        :rtype: ``list`` of :class:`Presentation`
        """
        return [Presentation(p, self._client)
                for p in self.options['presentations']]

    def get_presentation_data(self, presentation):
        """
        Get the data for a presentation object

        :param presentation: The presentation of this counter
        :type  presentation: :class:`Presentation`

        :rtype: ``dict``
        """
        return presentation.get_data()
