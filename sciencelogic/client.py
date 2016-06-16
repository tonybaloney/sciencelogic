# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
from device import Device


class Client(object):
    def __init__(self, username, password, uri, auto_connect=True):
        self.username = username
        self.password = password
        self.uri = uri
        
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        
        if auto_connect:
            self.sysinfo = self._connect()
    
    def _connect(self):
        r = self.get('api/sysinfo')
        return r.json()

    def get(self, uri):
        return self.session.get('%s/%s' % (self.uri, uri))

    def devices(self, details=False):
        cl = self.get('api/device%s' % '?extended_fetch=1' if details else '')
        devices = []
        for r in cl.json()['result_set']:
            devices.append(Device(r['URI'], r['description'], self, True))
        return devices
