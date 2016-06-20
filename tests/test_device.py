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
from sciencelogic.device import Device


class DeviceTestCase(unittest.TestCase):

    def test_device_bad_param(self):
        with self.assertRaises(TypeError):
            c = Device('potato!')

    def test_device_bad_values(self):
        with self.assertRaises(TypeError):
            c = Device('me','pass','potato!')

    def test_get_device(self):
        with requests_mock.mock() as m:
            m.get('https://test.com/api/sysinfo', text=self._load_fixture('fixtures/sysinfo.json'))
            m.get('https://test.com/api/device', text=self._load_fixture('fixtures/api_device_extended.json'))
            m.get('https://test.com/api/device/12345', text=self._load_fixture('fixtures/api_device_12345.json'))
            c = Client('my', 'test', 'https://test.com')
            device = c.get_device(12345)
            self.assertEquals(device.details['name'], 'AU9/kubernetes-master01')

    def test_get_device_counters(self):
        with requests_mock.mock() as m:
            m.get('https://test.com/api/sysinfo', text=self._load_fixture('fixtures/sysinfo.json'))
            m.get('https://test.com/api/device', text=self._load_fixture('fixtures/api_device_extended.json'))
            m.get('https://test.com/api/device/12345', text=self._load_fixture('fixtures/api_device_12345.json'))
            m.get('https://test.com/api/device/10857/performance_data', text=self._load_fixture('fixtures/api_device_12345_performance_data.json'))
            c = Client('my', 'test', 'https://test.com')
            device = c.get_device(12345)
            device.performance_counters()
            self.assertEquals(device.details['name'], 'AU9/kubernetes-master01')

    def _load_fixture(self, path):
        with open(os.path.join(os.getcwd(), 'tests', path), 'r') as fixture:
            f = fixture.read()
        return f

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
