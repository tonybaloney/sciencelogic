# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth


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
        r = self.session.get('%s/%s' % (self.uri, 'api/sysinfo'))
        return r.json()
