import requests
import json

base_url = 'http://localhost:5000/player'
headers = {"Content-Type": "application/json"}
payload = json.dumps({"name": "shaun", "country": "not_country", "id": 'all'})
payload2 = json.dumps({"name": "not shaun", "country": "yes", "id": 0})

re = requests.post(base_url, headers=headers, data=payload)
print('post', re.content)
data = json.dumps({"country": "dd"})
# g = requests.put('http://localhost:5000/api/update/1',  data=payload2, headers=headers)
g = requests.get(base_url, headers=headers, data=payload)
print('gettttttttt', g.content)
gg = requests.put(base_url, headers=headers, data=payload2)
print(g.content)
lol = json.loads(g.content)
if len(lol) > 2:
    print(lol[0]['data'])
print('dd')

# r = requests.get('http://localhost:5000/api/list',headers=headers)
# print(r.content)
