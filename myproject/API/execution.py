import json
import bearer
import requests
import re

URL = "https://us-4.rightscale.com/api/deployments?filter[]=name==[kcfn01-cfn02] - 06.07.00"
URL2 = "https://us-4.rightscale.com/api/right_scripts?filter[]=name==hostname"

# Server Array HREF for WFM

headers = {'X-API-Version': '1.5',
           'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + bearer.token}

r = requests.get(URL, headers=headers)
r2 = requests.get(URL2, headers=headers)


def execution_name():
    my_list = []
    for i in (json.loads(r.content)):
        if re.search("^WFM", i['name']):
            my_list.append('-'.join(i['name'].split("-", 3))[:-14])
            my_list.append(i['description'].split("[View in Self-Service]", 1)[1][1:74])
    return my_list


def server_array():
    my_list = []
    for i in (json.loads(r.content)):
        if re.search("^WFM", i['name']):
            array_href = i['links']
            for j in array_href:
                if j['rel'] == 'server_arrays':
                    my_list.append('https://us-4.rightscale.com' + j['href'])
    return my_list


def fnt_array():
    my_list = []
    for url in server_array():
        resp = requests.get(url, headers=headers)
        for i in (json.loads(resp.content)):
            if 'fnt' in i['name']:
                fnt_href = i['links']
                for j in fnt_href:
                    if j['rel'] == 'current_instances':
                        my_list.append('https://us-4.rightscale.com' + j['href'])
    return my_list


def bck_array():
    my_list = []
    for url in server_array():
        resp = requests.get(url, headers=headers)
        for i in (json.loads(resp.content)):
            if 'fnt' not in i['name']:
                fnt_href = i['links']
                for j in fnt_href:
                    if j['rel'] == 'current_instances':
                        my_list.append('https://us-4.rightscale.com' + j['href'])
    return my_list


def fnt_ip():
    my_list = []
    for url in fnt_array():
        resp = requests.get(url, headers=headers)
        for i in (json.loads(resp.content)):
            ip = i['links']
            for j in ip:
                if j['rel'] == 'self':
                    my_list.append('https://us-4.rightscale.com' + j['href'])
    return my_list


def bck_ip():
    my_list = []
    for url in bck_array():
        resp = requests.get(url, headers=headers)
        for i in (json.loads(resp.content)):
            ip = i['links']
            for j in ip:
                if j['rel'] == 'self':
                    my_list.append('https://us-4.rightscale.com' + j['href'])
    return my_list


def right_script():
    for i in (json.loads(r2.content)):
        if i['name'] == 'hostname':
            rs_href = i['links']
            for j in rs_href:
                if j['rel'] == 'self':
                    return j['href']
