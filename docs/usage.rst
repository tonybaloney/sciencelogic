=====
Usage
=====

To use PythonEM7 in a project::

    from sciencelogic.client import Client

    c = Client('jazz', 'hands!', 'https://au-monitoring.mcp-services.net/')
    
    # API details
    print(c.sysinfo)