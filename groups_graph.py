import requests
import json
import time
import networkx
import collections
import re

token = open('token.txt')
for line in token:
    token = line
ACCESS_TOKEN = token
group_get_count = "https://api.vk.com/method/groups.getById?group_id={}&fields=members_count&v=5.103&access_token={}"


def getGroupNameAndCount(group_id):
    json_resp = requests.get(
        group_get_count.format(group_id, ACCESS_TOKEN)).json()
    time.sleep(0.33)
    if json_resp.get('error'):
        print('error')
        return ('error', 0)
    else:
        print(json_resp['response'][0]['name'],
              json_resp['response'][0]['members_count'])
        return (json_resp['response'][0]['name'], json_resp['response'][0]['members_count'])


group_file = open('nenarusskom.txt', 'r')
group_list = []
for line in group_file:
    group = line.split('/')[3].split('\n')[0].replace(' ', '')
    if re.fullmatch(r'club\d+', group):
        group = group[4:]
    if re.fullmatch(r'public\d+', group):
        group = group[6:]
    group_list.append(group)

group_file.close()

g = networkx.Graph(directed=False)
for group in group_list:
    name, count = getGroupNameAndCount(group)
    g.add_node(group, name=name, count=count)

pairs_file = open('pairs.csv', 'r')
for line in pairs_file:
    (g1, g2) = line.split(',')
    g1 = g1.replace('\n', '')
    g2 = g2.replace('\n', '')
    if g.has_edge(g1, g2):
        g.edges[g1, g2]['weight'] += 1
    else:
        g.add_edge(g1, g2, weight=1)


g.remove_nodes_from(list(networkx.isolates(g)))

networkx.write_graphml(g, 'groups_graph.graphml')
