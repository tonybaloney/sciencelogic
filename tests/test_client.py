#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sciencelogic
----------------------------------

Tests for `sciencelogic` module.
"""
import os
import unittest
import requests_mock

from sciencelogic.client import Client


class ClientTestCase(unittest.TestCase):

    def test_client_bad_param(self):
        with self.assertRaises(TypeError):
            c = Client('potato!')

    def test_client_bad_values(self):
        with self.assertRaises(ValueError):
            c = Client('me','pass','potato!')

    def test_format_get(self):
        with requests_mock.mock() as m:
            m.get('https://test.com/api/sysinfo', text=self._load_fixture('fixtures/sysinfo.json'))
            m.get('https://test.com/api/device', text=self._load_fixture('fixtures/api_device.json'))
            c = Client('my', 'test', 'https://test.com')
            # prepended /
            info = c.get('/api/sysinfo').json()
            self.assertEquals(info['em7build'],'45945')

    def test_get_devices_no_details(self):
        with requests_mock.mock() as m:
            m.get('https://test.com/api/sysinfo', text=self._load_fixture('fixtures/sysinfo.json'))
            m.get('https://test.com/api/device', text=self._load_fixture('fixtures/api_device.json'))
            c = Client('my', 'test', 'https://test.com')
            devices = c.devices(details=False)
            self.assertEquals(len(devices), 11)

    def test_get_devices_details(self):
        with requests_mock.mock() as m:
            m.get('https://test.com/api/sysinfo', text=self._load_fixture('fixtures/sysinfo.json'))
            m.get('https://test.com/api/device', text=self._load_fixture('fixtures/api_device_extended.json'))
            c = Client('my', 'test', 'https://test.com')
            devices = c.devices(details=True)
            self.assertEquals(len(devices), 11)

    def _load_fixture(self, path):
        with open(os.path.join(os.getcwd(), 'tests', path), 'r') as fixture:
            f = fixture.read()
        return f

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
