import json
import requests

rs_token = 'f91957e9a091aff72ac841eb906103c907435b4a'
URL = 'https://us-4.rightscale.com/api/oauth2'

headers = {'X-API-Version': '1.5',
           'Content-Type': 'application/json'}

data = {'grant_type': 'refresh_token',
        'refresh_token': rs_token
        }

r = requests.post(URL, data=json.dumps(data), headers=headers)
token = json.loads(r.content)["access_token"]
