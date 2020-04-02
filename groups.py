import requests
import json
import time
import networkx
import collections
import re
import numpy as np

token = open('token.txt')
for line in token:
    token = line
ACCESS_TOKEN = token

group_get_members = "https://api.vk.com/method/groups.getMembers?group_id={}&offset={}&v=5.103&access_token={}"
# id,offset,token

group_get_count = "https://api.vk.com/method/groups.getById?group_id={}&fields=members_count&v=5.103&access_token={}"
#id, token

# открываем файл с названиями групп, выкачиваем id групп в массив
group_file = open('nenarusskom.txt', 'r')
group_list = []
for line in group_file:
    group = line.split('/')[3].split('\n')[0].replace(' ', '')
    if re.fullmatch(r'club\d+', group):
        group = group[4:]
    if re.fullmatch(r'public\d+', group):
        group = group[6:]
    group_list.append(group)

# получаем количество участников группы


def getGroupCount(group_id):
    json_resp = requests.get(
        group_get_count.format(group_id, ACCESS_TOKEN)).json()
    time.sleep(0.33)
    if json_resp.get('error'):
        print(json_resp)
        return 0
    else:
        print(json_resp['response'][0]['name'],
              json_resp['response'][0]['members_count'])
        return json_resp['response'][0]['members_count']


def getAllGroupMembers(group_id):
    group_count = getGroupCount(group_id)
    if group_count == 0:
        return list()
    offset = 0
    members = []
    cnt = 0
    # while (offset < group_count):
    #     members = members + requests.get(group_get_members.format(
    #         group_id, offset, ACCESS_TOKEN)).json()['response']['items']
    #     offset += 1000
    #     time.sleep(0.33)
    while(cnt*25000 < group_count):
        code = '''
        var offset = ''' + str(offset) + '''; 
        var group_id= "''' + str(group_id) + '''"; 
        var members; 
        var requests = 0; 
        var ret = [];
        while (requests<25) {
            members = API.groups.getMembers({"group_id": group_id, "offset": offset, "count": 1000});
            ret = ret + members.items;
            requests = requests+1;
            offset = offset+1000;
        }
        return ret;'''
        payload = {
            "code": code,
            "access_token": ACCESS_TOKEN,
            "v": '5.103',
        }
        req = requests.post('https://api.vk.com/method/execute', data=payload)
        cnt += 1
        members += req.json()['response']
        offset += 25000
        time.sleep(0.33)
    return members


result = open('table.csv', 'a')


# проходимся по каждой группе
for group in group_list:

    members = getAllGroupMembers(group)
    for member in members:
        result.write(str(group)+','+str(member)+'\n')

result.close()
