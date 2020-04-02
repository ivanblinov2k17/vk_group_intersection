import requests
import json
import time
import networkx
import collections
token = "569cca61dda3774ce0f2ec604e611f9a8ebdb6ffe61761dc2416bc38b20646b65a1ab3c286bbffcf11bc0"

url = "https://api.vk.com/method/friends.getOnline?v=5.103&access_token={}".format(
    token)


def get_friends_ids(user_id):
    friends_url = 'https://api.vk.com/method/friends.get?user_id={}&v=5.52&access_token={}'.format(
        user_id, token)
    json_response = requests.get(friends_url).json()
    time.sleep(0.33)
    if json_response.get('error'):
        print(json_response.get('error'))
        return list()

    return json_response['response']['items']


graph = {}
# ваш user id, для которого вы хотите построить граф друзей.
friend_ids = get_friends_ids(247405142)
for friend_id in friend_ids:
    print('Processing id: ', friend_id)
    graph[friend_id] = get_friends_ids(friend_id)

g = networkx.Graph(directed=False)
for i in graph:
    g.add_node(i)
    for j in graph[i]:
        if i != j and i in friend_ids and j in friend_ids:
            g.add_edge(i, j)

networkx.write_graphml(g, 'graph.graphml')
