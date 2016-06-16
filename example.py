from sciencelogic.client import Client

c = Client('a_user', 'a_password!', 'https://monitoring.services.net/')
print(c.sysinfo)