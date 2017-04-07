import requests
import json
payload = {'k1': 'v1', 'k2': 'v2'}
r = requests.post('http://httpbin.org/post', data=payload)
print(r.text)
r = requests.post('http://httpbin.org/post', data=json.dumps(payload))
print(r.text)
