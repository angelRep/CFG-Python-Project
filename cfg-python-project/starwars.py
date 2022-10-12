from typing import Any

start_id_number = 1
last_id_number = 83
stats = ['height', 'mass', 'vehicles', 'starships']


def get_stats():
    return stats


def compare(stat_name, user_stat_value, opponent_stat_value):
    user_stat_value = 0 if user_stat_value is None else user_stat_value
    opponent_stat_value = 0 if opponent_stat_value is None else opponent_stat_value

    if stat_name in [stats[2], stats[3]]:
        user_stat_value = user_stat_value * 100
        opponent_stat_value = opponent_stat_value * 100

    if user_stat_value > opponent_stat_value:
        return [1, user_stat_value]
    elif user_stat_value == opponent_stat_value:
        return [0, 0]
    else:
        return [-1, opponent_stat_value]


def get_url(sw_id):
    url = "https://swapi.dev/api/people/{}".format(sw_id)
    return url


def read_json(response, sw_id) -> dict[str, Any]:
    sw_character = response.json()

    return {
        'name': sw_character['name'],
        'height': int(sw_character['height']),
        'mass': float(sw_character['mass']) if sw_character['mass'].isnumeric() else 0.0,
        'vehicles': len(sw_character['vehicles']),
        'starships': len(sw_character['starships']),
        'available': 1,
    }


def print_details(sw_character):
    print('         NAME : {}'.format(sw_character['name']))
    print('       HEIGHT : {}'.format(sw_character['height']))
    print('         MASS : {}'.format(sw_character['mass']))
    print(' No. VEHICLES : {}'.format(sw_character['vehicles']))
    print('No. STARSHIPS : {}'.format(sw_character['starships']))
    print('    AVAILABLE : {}'.format(("NO" if sw_character['available'] == 0 else "YES")))

# 1 - 83
# url3 = "https://swapi.dev/api/people/5"
# response3 = requests.get(url3)
# star_war = response3.json()
# print(star_war['name'])
# print(star_war['height'])
# print(star_war['mass'])
# print(len(star_war['vehicles']))
# print(len(star_war['starships']))
