from typing import Any

start_id_number = 1
last_id_number = 997
stats = ['id', 'rank', 'popularity', 'score', 'favorites']


def get_stats():
    return stats


def compare(stat_name, user_stat_value, opponent_stat_value):
    user_stat_value = 0 if user_stat_value is None else user_stat_value
    opponent_stat_value = 0 if opponent_stat_value is None else opponent_stat_value

    if stat_name == stats[3]:
        user_stat_value = user_stat_value * 10
        opponent_stat_value = opponent_stat_value * 10

    # the highest rank is the smallest number
    if stat_name == stats[1]:
        if user_stat_value < opponent_stat_value:
            return [1, user_stat_value]
        elif user_stat_value == opponent_stat_value:
            return [0, 0]
        else:
            return [-1, opponent_stat_value]

    if user_stat_value > opponent_stat_value:
        return [1, user_stat_value]
    elif user_stat_value == opponent_stat_value:
        return [0, 0]
    else:
        return [-1, opponent_stat_value]


def get_url(anime_id):
    url = "https://api.jikan.moe/v4/anime/{}".format(anime_id)
    return url


def read_json(response, anime_id) -> dict[str, Any]:
    anime = response.json()

    return {
        'id': anime['data']['mal_id'],
        'title': anime['data']['title'],
        'rank': anime['data']['rank'],
        'popularity': anime['data']['popularity'],
        'score': anime['data']['score'],
        'favorites': anime['data']['favorites'],
        'available': 1,
    }


def text_details(anime):
    text = '        ID : {}'.format(anime['id'])
    text = text + '\n     TITLE : {}'.format(anime['title'])
    text = text + '\n      RANK : {}'.format(anime['rank'])
    text = text + '\nPOPULARITY : {}'.format(anime['popularity'])
    text = text + '\n     SCORE : {}'.format(anime['score'])
    text = text + '\n FAVORITES : {}'.format(anime['favorites'])
    text = text + '\n    AVAILABLE : {}'.format(("NO" if anime['available'] == 0 else "YES"))
    return text


def print_details(anime):
    print('        ID : {}'.format(anime['id']))
    print('     TITLE : {}'.format(anime['title']))
    print('      RANK : {}'.format(anime['rank']))
    print('POPULARITY : {}'.format(anime['popularity']))
    print('     SCORE : {}'.format(anime['score']))
    print(' FAVORITES : {}'.format(anime['favorites']))
    print(' AVAILABLE : {}'.format(("NO" if anime['available'] == 0 else "YES")))

# 1 - 997 some doesnt exist
# url1 = "https://api.jikan.moe/v4/anime/100"
# response = requests.get(url1)
# anime = response.json()
# print(anime['data']['mal_id'])
# print(anime['data']['title'])
# print(anime['data']['rank'])
# print(anime['data']['popularity'])
# print(anime['data']['score'])
# print(anime['data']['favorites'])
