from api import get_friends
import time


def get_network(users_ids, as_edgelist=True):
    user_num = 0
    if as_edgelist:  # ввиде списка ребер
        edge_list = []
        for user in users_ids:
            if user_num % 3 == 0:  # каждый третий запрос
                time.sleep(0.4)
            try:
                friend_list = get_friends(user, 'fields')
            except KeyError:
                continue
            else:
                for friend in friend_list:
                    if friend in users_ids:
                        edge_list.append((users_ids.index(user), users_ids.index(friend)))
                user_num += 1
        return edge_list
    else:
        matrix = [[0] * len(users_ids) for _ in range(len(users_ids))]
        for user in users_ids:
            if user_num % 3 == 0:
                time.sleep(0.4)
            try:
                friend_list = get_friends(user, 'fields')
            except KeyError:
                continue
            else:
                for friend in friend_list:
                    if friend in users_ids:
                        matrix[users_ids.index(user)][users_ids.index(friend)] = 1
                user_num += 1
        return matrix


def plot_graph(graph):
    pass
    # PUT YOUR CODE HERE
