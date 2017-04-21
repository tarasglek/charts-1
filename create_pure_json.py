import pure.cli.api.test as api
import json

tokens = api.pureadmin_list(name=[], api_token=True, expose=True)
# [{'created': datetime.datetime(2017, 3, 21, 19, 35, 4), 'name': 'root', 'expires': datetime.datetime(
#     1970, 1, 1, 0, 0), 'api_token': '9296c1ac-381f-402f-a129-fe64dd02adc9'}]

interfaces = api.purenetwork_list(name='linux.mgmt0')
# [{'address': '10.19.66.145',
#   'enabled': True,
#   'gateway': '10.19.66.1',
#   'hwaddr': '52:54:10:26:38:3d',
#   'master': False,
#   'mode': 'static',
#   'mtu': 1500,
#   'name': 'linux.mgmt0',
#   'netmask': '255.255.255.0',
#   'services': ['app'],
#   'slave': False,
#   'slaves': [],
#   'speed': 1000000000,
#   'vm_device': 'mgmt0',
#   'vport': 'MGMT_0'}]
output = {"FlashArrays":[{
  "MgmtEndPoint":interfaces[0]['address'],
  "APIToken":tokens[0]['api_token']
  }]}

print output
