============================================================
ScienceLogic - a Python library for the ScienceLogic EM7 API
============================================================

.. image:: https://img.shields.io/pypi/v/sciencelogic.svg
        :target: https://pypi.python.org/pypi/sciencelogic

.. image:: https://img.shields.io/travis/tonybaloney/sciencelogic.svg
        :target: https://travis-ci.org/tonybaloney/sciencelogic

.. image:: https://coveralls.io/repos/github/tonybaloney/sciencelogic/badge.svg?branch=master
        :target: https://coveralls.io/github/tonybaloney/sciencelogic?branch=master

.. image:: https://readthedocs.org/projects/sciencelogic/badge/?version=latest
        :target: https://readthedocs.org/projects/sciencelogic/?badge=latest
        :alt: Documentation Status


Client library for sciencelogic EM7

* Free software: MIT license
* Documentation: https://sciencelogic.readthedocs.org.

Usage
--------

To use Python EM7 in a project::
    from sciencelogic.client import Client

    
    c = Client('jazz', 'hands!', 'https://au-monitoring.mcp-services.net/')
    
    # API details
    print(c.sysinfo)

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
