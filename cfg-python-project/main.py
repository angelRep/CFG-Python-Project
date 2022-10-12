# Top Trumps
import random
from typing import Any
import requests
import pokemon as pkm
import harrypottercharacter as hp
import starwars as sw
import anime as ani
import manga as man

# from tkinter import *

# GLOBAL VARIABLES
user_cards = []
opponent_cards = []

themes = ["pokemon", "harry potter", "star wars", "anime", "manga"]
theme_selected = ""
theme_functions = ""

rounds = 0
cards_per_round = 0

user_score = 0
opponent_score = 0


def print_line():
    print()


# def print_pokemon(pokemon):
#     print('       ID : {}'.format(pokemon['id']))
#     print('     NAME : {}'.format(pokemon['name']))
#     print('   HEIGHT : {}'.format(pokemon['height']))
#     print('   WEIGHT : {}'.format(pokemon['weight']))
#     print('AVAILABLE : {}'.format(("NO" if pokemon['available'] == 0 else "YES")))


def print_cards(card_list):
    i = 0
    length = len(card_list)
    while i < length:
        print('CARD {}'.format(i + 1))
        # print_pokemon(card_list[i])
        theme_functions.print_details(card_list[i])
        print_line()
        i = i + 1


def check_top_results(new_score):
    is_new_top_score = False
    top_scores = []
    scores_length = 0

    try:
        with open('top_scores.txt', 'r') as top_scores_file:
            contents = top_scores_file.read()
    except FileNotFoundError:
        contents = ""

    if contents != "":
        top_scores = contents.split(", ")
        top_scores = [float(numeric_string) for numeric_string in top_scores]
        scores_length = len(top_scores)

    # check if it's a new top score
    if scores_length < 10:
        top_scores.append(new_score)
        top_scores.sort(reverse=True)  # sort in descending order
        is_new_top_score = True
    else:
        i = 0

        while i < scores_length:
            if top_scores[i] < new_score:
                top_scores.insert(i, new_score)
                is_new_top_score = True
                top_scores.pop()  # remove the min previous score
                pass

            i = i + 1

    # in case new score is not among the top 10 scores, return
    if not is_new_top_score:
        return

    with open('top_scores.txt', 'w+') as top_scores_file:
        top_scores = [str(element) for element in top_scores]
        scores = ", ".join(top_scores)
        print_line()
        print_line()
        print("(っ◔◡◔)っ ♥ NEW TOP SCORE!!! --> {} ♥\nThe top scores are: {}".
              format(new_score, scores))
        top_scores_file.write(scores)


def random_number(start, end):
    return random.randint(start, end)


def get_random_item() -> dict[str, Any]:
    # pokemon_id = random.randint(1, 151)
    # url = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon_id)
    # response = requests.get(url)
    # pokemon = response.json()
    #
    # return {
    #     'name': pokemon['name'],
    #     'id': pokemon['id'],
    #     'height': pokemon['height'],
    #     'weight': pokemon['weight'],
    #     'available': 1,
    # }
    response = ""
    item_id = 0
    response_status = 0
    while response_status != 200:
        item_id = random_number(theme_functions.start_id_number, theme_functions.last_id_number)
        response = requests.get(theme_functions.get_url(item_id))
        response_status = response.status_code
        print("RESPONSE STATUS: {}".format(response_status))

    return theme_functions.read_json(response, item_id)


def prepare_cards(cards_number):
    i = 0
    card_list = []
    while i < cards_number:
        card_list.append(get_random_item())
        i = i + 1

    return card_list


def game_round():
    plays = 1
    opponent_turn = random.randint(0, 1)
    selected_stat = ""

    while plays <= cards_per_round:
        print("Here are your cards:")
        print_cards(user_cards)

        # Select opponent's card
        opponent_card_select = random.randint(0, len(opponent_cards) - 1)

        while opponent_cards[opponent_card_select]['available'] == 0:
            opponent_card_select = random.randint(0, len(opponent_cards) - 1)

        # Opponent selects stat if it's his turn
        if opponent_turn == 1:
            # selected_stat = random.choice(['id', 'height', 'weight'])
            selected_stat = random.choice(theme_functions.get_stats())
            print('Opponent plays first! The stat that has been selected is {}'
                  .format(selected_stat))

        # Select player's card
        print('Your turn!' if opponent_turn == 1 else 'You play first!')
        user_card_select = int(input("Choose a card number: ")) - 1

        while user_card_select < 0 or user_card_select >= len(user_cards) or \
                user_cards[user_card_select]['available'] == 0:
            user_card_select = int(input("Card number is out of range or has been used.\n"
                                         "Choose a card number: ")) - 1

        # print_pokemon(user_cards[user_card_select])
        theme_functions.print_details(user_cards[user_card_select])

        # Select a stat
        if opponent_turn == 0:
            # selected_stat = input("Select a stat: (id, height, weight) ")
            selected_stat = input("Select a stat: {} ".format(theme_functions.get_stats()))
            selected_stat = selected_stat.lower()

            # while selected_stat not in ['id', 'height', 'weight']:
            while selected_stat not in theme_functions.get_stats():
                # selected_stat = input("Try again! It should be id, height or weight: ")
                selected_stat = input("Try again! It should be {}: ".format(theme_functions.get_stats()))
                selected_stat = selected_stat.lower()

        print_line()

        # if user_cards[user_card_select][selected_stat] > opponent_cards[opponent_card_select][selected_stat]:
        #     global user_score
        #     user_score = user_score + user_cards[user_card_select][selected_stat]
        #     opponent_turn = 0
        #     print("Congratulations! You won!")
        # elif user_cards[user_card_select][selected_stat] < opponent_cards[opponent_card_select][selected_stat]:
        #     global opponent_score
        #     opponent_score = opponent_score + opponent_cards[opponent_card_select][selected_stat]
        #     opponent_turn = 1
        #     print("You lose...")
        # else:
        #     opponent_turn = random.randint(0, 1)
        #     print("It's a draw!")

        compare_result = theme_functions.compare(selected_stat, user_cards[user_card_select][selected_stat],
                                                 opponent_cards[opponent_card_select][selected_stat])

        if compare_result[0] == 1:
            global user_score
            user_score = user_score + compare_result[1]
            opponent_turn = 0
            print("Congratulations! You won!")
        elif compare_result[0] == -1:
            global opponent_score
            opponent_score = opponent_score + compare_result[1]
            opponent_turn = 1
            print("You lose...")
        else:
            opponent_turn = random.randint(0, 1)
            print("It's a draw!")

        print("Your card's {} is {}."
              .format(selected_stat, user_cards[user_card_select][selected_stat]))
        print("Opponent's card's {} is {}."
              .format(selected_stat, opponent_cards[opponent_card_select][selected_stat]))
        print_line()

        # Set pokemon to unavailable
        user_cards[user_card_select]['available'] = 0
        opponent_cards[opponent_card_select]['available'] = 0

        plays = plays + 1


def game():
    game_number = 1
    while game_number <= rounds:
        print("Please wait! The game is getting prepared...")

        global user_cards, opponent_cards, user_score, opponent_score

        user_cards = prepare_cards(cards_per_round)
        opponent_cards = prepare_cards(cards_per_round)

        print("Ok! Let's start!")
        print('ROUND {}\n=========='.format(game_number))
        game_round()

        print_line()
        print_line()
        print('+----------------------+')
        print('| RESULTS FOR ROUND {}  |'.format(game_number))
        print('+----------------------+')
        print('Your score is: {}'.format(user_score))
        print('Opponent\'s score is: {}'.format(opponent_score))
        if user_score > opponent_score:
            print('Congratulations! You won this round!')
            check_top_results(user_score)
        elif user_score < opponent_score:
            print('You lost this round...')
        else:
            print('It\'s a draw')
        # print('Congratulations! You won this round!' if user_score > opponent_score else
        #       'You lost this round...' if user_score < opponent_score
        #       else 'It\'s a draw')
        print_line()
        print_line()

        game_number = game_number + 1

        # Resetting
        user_score = 0
        opponent_score = 0
        user_cards = []
        opponent_cards = []


while rounds < 1 or rounds > 10:
    rounds = int(input("Number of rounds (1 - 10): "))

while cards_per_round < 1 or cards_per_round > 10:
    cards_per_round = int(input("Number of cards per round (1 - 10): "))

while theme_selected not in themes:
    theme_selected = input("Card's Theme (Pokemon, Harry Potter, Star Wars, Anime, Manga): ")
    theme_selected = theme_selected.lower()

if theme_selected == themes[0]:  # Pokemon
    theme_functions = pkm
elif theme_selected == themes[1]:  # Harry Potter
    theme_functions = hp
elif theme_selected == themes[2]:  # Star Wars
    theme_functions = sw
elif theme_selected == themes[3]:  # Anime
    theme_functions = ani
elif theme_selected == themes[4]:  # Manga
    theme_functions = man
else:
    theme_functions = pkm  # Default theme is pokemon

game()

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

# 1 - 83
# url3 = "https://swapi.dev/api/people/5"
# response3 = requests.get(url3)
# star_war = response3.json()
# print(star_war['name'])
# print(star_war['height'])
# print(star_war['mass'])
# print(len(star_war['vehicles']))
# print(len(star_war['starships']))

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
