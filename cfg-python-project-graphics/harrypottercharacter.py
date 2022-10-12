from typing import Any

start_id_number = 1
last_id_number = 400
stats = ['yearofbirth', 'wizard', 'ancestry', 'student', 'staff', 'alive']


def get_stats():
    return stats


def compare(stat_name, user_stat_value, opponent_stat_value):
    if stat_name != stats[2]:
        user_stat_value = 0 if user_stat_value is None else user_stat_value
        opponent_stat_value = 0 if opponent_stat_value is None else opponent_stat_value

    if user_stat_value == "":
        user_stat_value = 0
    if opponent_stat_value == "":
        opponent_stat_value = 0
    if stat_name == stats[0]:
        user_value = user_stat_value
        opponent_value = opponent_stat_value
    elif stat_name in [stats[1], stats[3], stats[4], stats[5]]:
        user_value = 100 if user_stat_value else 0
        opponent_value = 100 if opponent_stat_value else 0
    elif stat_name == stats[2]:
        user_value = 400 if user_stat_value == "pure-blood" \
            else 200 if user_stat_value == "half-blood" else 0
        opponent_value = 400 if opponent_stat_value == "pure-blood" \
            else 200 if opponent_stat_value == "half-blood" else 0

    if user_value > opponent_value:
        return [1, user_value]
    elif user_value == opponent_value:
        return [0, 0]
    else:
        return [-1, opponent_value]


def get_url(hp_id):
    url = "https://hp-api.herokuapp.com/api/characters"
    return url


def read_json(response, hp_id) -> dict[str, Any]:
    hp_characters = response.json()
    hp_character = hp_characters[hp_id]

    return {
        'name': hp_character['name'],
        'yearofbirth': hp_character['yearOfBirth'],
        'species': hp_character['species'],
        'wizard': hp_character['wizard'],
        'ancestry': hp_character['ancestry'],
        'student': hp_character['hogwartsStudent'],
        'staff': hp_character['hogwartsStaff'],
        'alive': hp_character['alive'],
        'available': 1,
    }


def text_details(hp_character):
    text = '      NAME : {}'.format(hp_character['name'])
    text = text + '\nBIRTH YEAR : {}'.format(hp_character['yearofbirth'])
    text = text + '\n   SPECIES : {}'.format(hp_character['species'])
    text = text + '\n    WIZARD : {}'.format(hp_character['wizard'])
    text = text + '\n  ANCESTRY : {}'.format(hp_character['ancestry'])
    text = text + '\n   STUDENT : {}'.format(hp_character['student'])
    text = text + '\n     STAFF : {}'.format(hp_character['staff'])
    text = text + '\n     ALIVE : {}'.format(hp_character['alive'])
    text = text + '\n AVAILABLE : {}'.format(("NO" if hp_character['available'] == 0 else "YES"))
    return text


def print_details(hp_character):
    print('      NAME : {}'.format(hp_character['name']))
    print('BIRTH YEAR : {}'.format(hp_character['yearofbirth']))
    print('   SPECIES : {}'.format(hp_character['species']))
    print('    WIZARD : {}'.format(hp_character['wizard']))
    print('  ANCESTRY : {}'.format(hp_character['ancestry']))
    print('   STUDENT : {}'.format(hp_character['student']))
    print('     STAFF : {}'.format(hp_character['staff']))
    print('     ALIVE : {}'.format(hp_character['alive']))
    print(' AVAILABLE : {}'.format(("NO" if hp_character['available'] == 0 else "YES")))

# 1 - 400
# url4 = "https://hp-api.herokuapp.com/api/characters"
# response3 = requests.get(url4)
# hp_characters = response3.json()
# hp_character = hp_characters[5]
# print(hp_character)
# print(hp_character['name'])
# print(hp_character['yearOfBirth'])
# print(hp_character['species'])
# print(hp_character['wizard'])
# print(hp_character['ancestry'])
# print(hp_character['hogwartsStudent'])
# print(hp_character['hogwartsStaff'])
# print(hp_character['alive'])
