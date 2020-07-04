import json
import requests
import re
from api import api
from beans.User import RS_URL
from beans.Deployment import Deployment1


def execute_right_script(list_of_selected_deployments, rs_name, bearer_token):
    print("inside execute rightscript")
    print(rs_name)
    print(RS_URL)
    print(list_of_selected_deployments)
    headers = {'X-API-Version': '1.5',
               'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    list_of_ins_href = bck_ip(list_of_selected_deployments, headers)

    list_of_rs_response = []
    for bck_ins_href in list_of_ins_href:
        url = bck_ins_href + '/run_executable'
        rs_href = right_script(rs_name, headers)
        data = {"right_script_href": rs_href}
        print(url)
        print(rs_href)
        response = api.post(url, data, headers)
        list_of_rs_response.append(response)

    return list_of_rs_response


def bck_ip(list_of_selected_deployments, headers):
    my_list = []
    for url in bck_array(list_of_selected_deployments, headers):
        resp = requests.get(url, headers=headers)
        for i in (json.loads(resp.content)):
            ip = i['links']
            for j in ip:
                if j['rel'] == 'self':
                    my_list.append('https://us-4.rightscale.com' + j['href'])
    return my_list


def bck_array(list_of_selected_deployments, headers):
    my_list = []
    for url in server_array(list_of_selected_deployments, headers):
        resp = requests.get(url, headers=headers)
        for i in (json.loads(resp.content)):
            if 'fnt' not in i['name']:
                fnt_href = i['links']
                for j in fnt_href:
                    if j['rel'] == 'current_instances':
                        my_list.append('https://us-4.rightscale.com' + j['href'])
    return my_list


def server_array(list_of_selected_deployments, headers):
    my_list = []
    for deployment in list_of_selected_deployments:
        URL = RS_URL + 'api/deployments?filter[]=name==' + deployment
        r = requests.get(URL, headers=headers)
        for i in (json.loads(r.content)):
            if re.search("^WFM", i['name']):
                array_href = i['links']
                for j in array_href:
                    if j['rel'] == 'server_arrays':
                        my_list.append('https://us-4.rightscale.com' + j['href'])
    return my_list


def right_script(rs_name, headers):
    rs_href = ""
    URL = "https://us-4.rightscale.com/api/right_scripts?filter[]=name==" + rs_name
    r = requests.get(URL, headers=headers)
    for i in (json.loads(r.content)):
        if i['name'] == rs_name:
            rs_href = i['links']
            for j in rs_href:
                if j['rel'] == 'self':
                    rs_href = j['href']
    return rs_href


##############################################################################################
# Receives bearer token, environment, release version, service from Router                   #
# Creates URL with ENV and release version, and use URL in further execution name method     #
# Uses bearer token to authenticate                                                          #
# Returns list of Deployment objects                                                         #
##############################################################################################
def get_deployment_details(env, rel_version,service, bearer_token):
    print("get_deployment_details method in controller")
    
    if("cfn" in env):
        print("inside env.contains")
        account = '106388'
    
    URL     = "https://us-4.rightscale.com/api/tags/by_tag"
    headers = {'X-API-Version': '1.5',
               'Content-Type': 'application/json',
               'X-Account': account,
               'Authorization': 'Bearer ' + bearer_token}
    data    =   {"match_all": "true",
                 "resource_type": "deployments",
                 "tags": ["kronos:environment_name=" + env,
                          "kronos:shared_service_type=" + service,
                          "kronos:service_version=" + rel_version]
                 }
    
    r = requests.post(URL, headers=headers, json=data)
    print(r.content)
#    r = requests.get(URL, headers=headers)
#    list_of_dep_objects = execution_name(r)
    list_of_dep_objects=[]
    return list_of_dep_objects


def execution_name(r):
    my_list = []
    dep_name_list = []
    dep_url_list = []
    dep_obj_list = []
    for i in (json.loads(r.content)):
        if re.search("^WFM", i['name']):
            my_list.append('-'.join(i['name'].split("-", 3))[:-14])
            dep_name_list.append('-'.join(i['name'].split("-", 3))[:-14])
            my_list.append(i['description'].split("[View in Self-Service]", 1)[1][1:74])
            dep_url_list.append(i['description'].split("[View in Self-Service]", 1)[1][1:74])

    # separating out name and URL lists and creating a list of Deployment objects
    length = len(dep_name_list)
    for i in range(length):
        name = dep_name_list[i]
        url = dep_url_list[i]
        obj = Deployment1(name, url)
        dep_obj_list.append(obj.toJSON())

    return dep_obj_list
