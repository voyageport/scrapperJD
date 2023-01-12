import requests
from requests.auth import HTTPBasicAuth

url = "http://test.supplier.voyageport.com/product/cabins"


payload={'boat_id': '26',
'number': '3'}
files=[

]

headers = {
  'Token': '4d673d3d', #'4d544532',
  'Authorization': 'Basic aW5mb0B2b3lhZ2Vwb3J0LmNvbTpNM3Q0JTRkbTFuIzIw',
  'Cookie': 'laravel_session=eyJpdiI6InVpV2x3T1lJTWszOTE0eElLSGUxZ2c9PSIsInZhbHVlIjoidHZDTFdKdE9zZXRobUF4T0ZtRWRHaE00SSsyeTFPMXUyNHFZTng1enNDOHljYlY1TG5LeHVaYVp3R2hsSDFUMSIsIm1hYyI6IjQ4MWU2N2VjNzA0ODdiNGJiNTlhOTk1M2VlNTZmYmY3MDYxMjVlYWQxNDVlODBiYmI2MTAwMTA2OWEyNjk4MjEifQ%3D%3D'
}
"""

headers = {
            "Content-Type": "application/json",
            "Token": '4d673d3d'
        }
"""

response = requests.request("POST", url, auth=HTTPBasicAuth('user@voyageport.com', 'userVoy#1534'), headers=headers, data=payload, files=files)

"""
response = requests.post(url, json=payload,
                                 auth=HTTPBasicAuth('user@voyageport.com', 'userVoy#1534'),
                                 headers=headers)
"""

cabin_id = response.text
cabin_id = cabin_id.split('"id":')
cabin_id = cabin_id[1].split(',')
cabin_id = int(cabin_id[0])

print(cabin_id)

