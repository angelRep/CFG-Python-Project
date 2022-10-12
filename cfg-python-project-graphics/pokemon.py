from typing import Any

start_id_number = 1
last_id_number = 151
stats = ['id', 'height', 'weight']


def get_stats():
    return stats


def compare(stat_name, user_stat_value, opponent_stat_value):
    user_stat_value = 0 if user_stat_value is None else user_stat_value
    opponent_stat_value = 0 if opponent_stat_value is None else opponent_stat_value

    if user_stat_value > opponent_stat_value:
        return [1, user_stat_value]
    elif user_stat_value == opponent_stat_value:
        return [0, 0]
    else:
        return [-1, opponent_stat_value]


def get_url(pokemon_id):
    url = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon_id)
    return url


def read_json(response, pokemon_id) -> dict[str, Any]:
    pokemon = response.json()

    return {
        'name': pokemon['name'],
        'id': pokemon['id'],
        'height': pokemon['height'],
        'weight': pokemon['weight'],
        'available': 1,
    }


def text_details(pokemon):
    text = '       ID : {}'.format(pokemon['id'])
    text = text + '\n     NAME : {}'.format(pokemon['name'])
    text = text + '\n   HEIGHT : {}'.format(pokemon['height'])
    text = text + '\n   WEIGHT : {}'.format(pokemon['weight'])
    text = text + '\nAVAILABLE : {}'.format(("NO" if pokemon['available'] == 0 else "YES"))
    return text


def print_details(pokemon):
    print('       ID : {}'.format(pokemon['id']))
    print('     NAME : {}'.format(pokemon['name']))
    print('   HEIGHT : {}'.format(pokemon['height']))
    print('   WEIGHT : {}'.format(pokemon['weight']))
    print('AVAILABLE : {}'.format(("NO" if pokemon['available'] == 0 else "YES")))
