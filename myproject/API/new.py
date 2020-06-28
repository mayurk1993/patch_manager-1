from bearer import *
import re

URL = "https://us-4.rightscale.com/api/tags/by_tag"
service = "wfm"
env = "cfn02"
version = "06.07.00"

headers = {'X-API-Version': '1.5',
           'Content-Type': 'application/json',
           'X-Account': '106388',
           'Authorization': 'Bearer ' + token}

data = {"match_all": "true",
        "resource_type": "deployments",
        "tags": ["kronos:environment_name=" + env,
                 "kronos:shared_service_type=" + service,
                 "kronos:service_version=" + version]
        }

r = requests.post(URL, headers=headers, json=data)


# print(json.loads(r.content))


def server_array():
    my_list = []
    for i in (json.loads(r.content)):
        if 'tags' in i:
            array_href = i['links']
            for j in array_href:
                if j['rel'] == 'resource':
                    my_list.append('https://us-4.rightscale.com' + j['href'] + '/server_arrays')
    return my_list


print(server_array())
