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


def get_url(manga_id):
    url = "https://api.jikan.moe/v4/manga/{}".format(manga_id)
    return url


def read_json(response, manga_id) -> dict[str, Any]:
    manga = response.json()

    return {
        'id': manga['data']['mal_id'],
        'title': manga['data']['title'],
        'rank': manga['data']['rank'],
        'popularity': manga['data']['popularity'],
        'score': manga['data']['score'],
        'favorites': manga['data']['favorites'],
        'available': 1,
    }


def print_details(manga):
    print('        ID : {}'.format(manga['id']))
    print('     TITLE : {}'.format(manga['title']))
    print('      RANK : {}'.format(manga['rank']))
    print('POPULARITY : {}'.format(manga['popularity']))
    print('     SCORE : {}'.format(manga['score']))
    print(' FAVORITES : {}'.format(manga['favorites']))
    print(' AVAILABLE : {}'.format(("NO" if manga['available'] == 0 else "YES")))

# 1 - 997 some doesnt exist
# url2 = "https://api.jikan.moe/v4/manga/100"
# response2 = requests.get(url2)
# manga = response2.json()
# print(manga['data']['mal_id'])
# print(manga['data']['title'])
# print(manga['data']['rank'])
# print(manga['data']['popularity'])
# print(anime['data']['score'])
# print(manga['data']['favorites'])
