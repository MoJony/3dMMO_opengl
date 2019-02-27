import requests
import json

base_url = 'http://localhost:5000/api/add'
headers = {"Content-Type": "application/json"}
payload = json.dumps({"name": "shaun", "country": "australia", "age": 24})
payload2 = json.dumps({"country": "new zealand"})

requests.post(base_url, headers=headers, data=payload)
data = json.dumps({"country": "dd"})
# g = requests.put('http://localhost:5000/api/update/1',  data=payload2, headers=headers)
g = requests.put('http://localhost:5000/api/update/1', json={"country": "new zealand"})
print(g.content)
print('dd')

r = requests.get('http://localhost:5000/api/list',headers=headers)
print(r.content)
