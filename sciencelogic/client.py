# -*- coding: utf-8 -*-
from requests.auth import HTTPBasicAuth
from sciencelogic.device import Device
import requests

requests.packages.urllib3.disable_warnings()


class Client(object):
    def __init__(self, username, password, uri,
                 auto_connect=True, verify_ssl=False):
        """
        Instantiate a EM7 Client API

        :param username: Your username
        :type  username: ``str``

        :param password: Your password
        :type  password: ``str``

        :param uri: The EM7 URI (excluding the /api)
        :param uri: ``str``

        :param auto_connect: Try an connect and get API data when initializing
        :param auto_connect: ``bool``
        """
        self.username = username
        self.password = password
        self.uri = uri
        self.verify = verify_ssl
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)

        if auto_connect:
            self.sysinfo = self._connect()

    def _connect(self):
        info = self.get('api/sysinfo')
        return info.json()

    def get(self, uri, params=None):
        """
        Get a URI from the API

        :param uri: The URI
        :type  uri: ``str``

        :params params: Extra params
        :type   params: ``dict``
        """
        if params is None:
            params = {}
        if uri.startswith('/'):
            uri = uri[1:]
        return self.session.get('%s/%s' % (self.uri, uri),
                                params=params,
                                verify=self.verify)

    def devices(self, details=False):
        """
        Get a list of devices

        :param details: Get the details of the devices
        :type  details: ``bool``

        :rtype: ``list`` of :class:`Device`
        """
        response = self.get('api/device', {'extended_fetch': 1}
                            if details else {})
        devices = []
        if details:
            for uri, device in response.json()['result_set'].items():
                devices.append(Device(device, uri, self, True))
        else:
            for device in response.json()['result_set']:
                devices.append(Device(device, device['URI'], self, False))
        return devices

    def get_device(self, device_id):
        """
        Get a devices

        :param device_id: The id of the device
        :type  device_id: ``int``

        :rtype: ``list`` of :class:`Device`
        """
        if not isinstance(device_id, int):
            raise TypeError('Device ID must be integer')
        uri = 'api/device/%s' % device_id
        device = self.session.get('%s/%s' % (self.uri, uri)).json()
        return Device(device, uri, self, True)
