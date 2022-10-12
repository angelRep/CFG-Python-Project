# Top Trumps
import random
from typing import Any
import requests
import pokemon as pkm
import harrypottercharacter as hp
import starwars as sw
import anime as ani
import manga as man

from tkinter import *

# GLOBAL VARIABLES
user_cards = []
opponent_cards = []

available_ids = ['-']

themes = ["pokemon", "harry potter", "star wars", "anime", "manga"]
theme_selected = ""
theme_functions = pkm

rounds = 0
cards_per_round = 0

user_score = 0
opponent_score = 0


def get_available_card_ids():
    index = 0
    ret_array = []

    while index < len(user_cards):
        if user_cards[index]['available'] == 1:
            ret_array.append(index + 1)
        index = index + 1

    return ret_array


def print_cards(card_labels, card_list):
    i = 0
    length = len(card_list)
    while i < length:
        if card_list[i]['available'] == 1:
            item_string = '----------------------------------\n' \
                          'CARD {}\n'.format(i + 1)
            item_string += theme_functions.text_details(card_list[i])
            item_string += "\n----------------------------------"
            card_labels[i].config(text=item_string)
        else:
            card_labels[i].config(text="")
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
        added = False

        # check if it's a new top score and the length is already 10
        while i < scores_length and not added:
            if top_scores[i] < new_score:
                top_scores.insert(i, new_score)
                is_new_top_score = True
                top_scores.pop()  # remove the min previous score
                added = True

            i = i + 1

    # in case new score is not among the top 10 scores, return
    if not is_new_top_score:
        return ""

    with open('top_scores.txt', 'w+') as top_scores_file:
        top_scores = [str(element) for element in top_scores]
        scores = ", ".join(top_scores)
        top_scores_string = "\n\n(っ◔◡◔)っ ♥ NEW TOP SCORE!!! --> {} ♥\nThe top scores are: {}".format(new_score, scores)
        top_scores_file.write(scores)

    return top_scores_string


def random_number(start, end):
    return random.randint(start, end)


def get_random_item() -> dict[str, Any]:
    response = ""
    item_id = 0
    response_status = 0
    while response_status != 200:
        item_id = random_number(theme_functions.start_id_number, theme_functions.last_id_number)
        response = requests.get(theme_functions.get_url(item_id))
        response_status = response.status_code

    return theme_functions.read_json(response, item_id)


def prepare_cards(cards_number):
    i = 0
    card_list = []
    while i < cards_number:
        card_list.append(get_random_item())
        i = i + 1

    return card_list


def game_round(game_window):
    global available_ids

    plays = 1
    opponent_turn = random.randint(0, 1)
    selected_stat = ""

    card_text_top = Label(game_window, text="")
    card_text_top.pack(anchor=CENTER)

    card_labels = []
    j = 0
    while j < cards_per_round:
        label_card = Label(game_window, text="CARD {}\nLoading...".format(j + 1))
        card_labels.append(label_card)
        card_labels[j].pack(side=TOP)
        j += 1

    label_1 = Label(game_window, text="")
    label_1.pack(anchor=CENTER)
    label_2 = Label(game_window, text="")
    label_2.pack(anchor=CENTER)

    available_ids = get_available_card_ids()
    card_select = Label(game_window, text="Card's Number:")
    card_id_var = StringVar(game_window)
    card_id_var.set(available_ids[0])
    card_select_num = OptionMenu(game_window, card_id_var, *available_ids)
    card_select.pack(anchor=CENTER)
    card_select_num.pack(anchor=CENTER)
    stat_options = theme_functions.get_stats()
    stat_select = Label(game_window, text="Select a stat:")
    stat_var = StringVar(game_window)
    stat_var.set(stat_options[0])
    stat_selection = OptionMenu(game_window, stat_var, *stat_options)
    stat_select.pack(anchor=CENTER)
    stat_selection.pack(anchor=CENTER)

    var = IntVar()
    button_play = Button(game_window, text="START ROUND", fg="white", bg="green", command=lambda: var.set(1))
    button_play.pack(anchor=CENTER)
    button_play.wait_variable(var)

    label_play_result = Label(game_window, text="")
    label_play_result.pack(anchor=CENTER)

    while plays <= cards_per_round:
        card_text_top.config(text="Here are your cards:")
        print_cards(card_labels, user_cards)

        # Select opponent's card
        opponent_card_select = random.randint(0, len(opponent_cards) - 1)

        while opponent_cards[opponent_card_select]['available'] == 0:
            opponent_card_select = random.randint(0, len(opponent_cards) - 1)

        # Opponent selects stat if it's his turn
        if opponent_turn == 1:
            selected_stat = random.choice(theme_functions.get_stats())
            stat_var.set(selected_stat)
            stat_selection.config(state=DISABLED)
            label_1.config(text='Opponent plays first! The stat that has been selected is {}'.format(selected_stat))
        else:
            label_1.config(text="")
            stat_selection.config(state=NORMAL)

        # Select player's card
        label_2.config(text='Your turn!' if opponent_turn == 1 else 'You play first!')

        button_play.config(text="PLAY")
        button_play.wait_variable(var)

        # take user inputs
        user_card_select = int(card_id_var.get()) - 1
        if opponent_turn == 0:
            selected_stat = str(stat_var.get())

        compare_result = theme_functions.compare(selected_stat, user_cards[user_card_select][selected_stat],
                                                 opponent_cards[opponent_card_select][selected_stat])

        if compare_result[0] == 1:
            global user_score
            user_score = user_score + compare_result[1]
            opponent_turn = 0
            playing_result = "Congratulations! You won!"
        elif compare_result[0] == -1:
            global opponent_score
            opponent_score = opponent_score + compare_result[1]
            opponent_turn = 1
            playing_result = "You lose..."
        else:
            opponent_turn = random.randint(0, 1)
            playing_result = "It's a draw!"

        playing_result += "\n"
        playing_result += "Your card's {} is {}." \
            .format(selected_stat, user_cards[user_card_select][selected_stat])
        playing_result += "Opponent's card's {} is {}." \
            .format(selected_stat, opponent_cards[opponent_card_select][selected_stat])
        playing_result += "\n"

        label_play_result.config(text=playing_result)

        # Update card number select list
        available_ids = get_available_card_ids()
        r_index = available_ids.index(int(card_id_var.get()))
        # r_index = card_select_num['menu'].get(int(card_id_var.get()))
        card_select_num['menu'].delete(r_index)
        card_id_var.set(card_select_num['menu'].entrycget(0, "label"))

        # Set item to unavailable
        user_cards[user_card_select]['available'] = 0
        opponent_cards[opponent_card_select]['available'] = 0

        plays = plays + 1

    button_play['state'] = DISABLED


def game():
    game_number = 1

    while game_number <= rounds:
        game_window = Toplevel(screen)
        game_window.geometry("700x900")
        game_window.title('ROUND {}'.format(game_number))
        label_top = Label(game_window, text="Please wait! The game is getting prepared...")
        label_top.pack(anchor=CENTER)

        global user_cards, opponent_cards, user_score, opponent_score

        user_cards = prepare_cards(cards_per_round)
        opponent_cards = prepare_cards(cards_per_round)

        label_top.config(text="Ok! Let's start! Press the button ''START ROUND''")
        game_round(game_window)

        result_string = '\n\n+--------------------------+'
        result_string = result_string + '\n| RESULTS FOR ROUND {}  |'.format(game_number)
        result_string = result_string + '\n+--------------------------+'
        result_string = result_string + '\nYour score is: {}'.format(user_score)
        result_string = result_string + '\nOpponent\'s score is: {}'.format(opponent_score)

        if user_score > opponent_score:
            result_string = result_string + '\nCongratulations! You won this round!'
            result_string = result_string + check_top_results(user_score)
        elif user_score < opponent_score:
            result_string = result_string + '\nYou lost this round...'
        else:
            result_string = result_string + '\nIt\'s a draw'

        result_string = result_string + '\n\n'

        label_result = Label(game_window, text=result_string)
        label_result.pack(anchor=CENTER)

        game_number = game_number + 1

        # Resetting
        user_score = 0
        opponent_score = 0
        user_cards = []
        opponent_cards = []


def start_button_click(num_rounds, num_cards, sel_theme="pokemon"):
    global theme_selected, rounds, cards_per_round, theme_functions

    rounds = num_rounds
    cards_per_round = num_cards
    theme_selected = sel_theme

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


screen = Tk()
screen.title("TOP TRUMPS")
screen.geometry("500x500")

welcome_text = Label(screen, text="Welcome to Top Trumps Game", fg="black", bg="white")

rounds_text = Label(screen, text="Number of rounds:")
entry_rounds = Scale(screen, from_=1, to=10, length=150, orient=HORIZONTAL)

cards_text = Label(screen, text="Number of cards per round:")
entry_cards = Scale(screen, from_=1, to=10, length=150, orient=HORIZONTAL)

theme_text = Label(screen, text="Card's Theme:")
theme_var = StringVar(screen)
theme_var.set(themes[0])
entry_theme = OptionMenu(screen, theme_var, *themes)

click_me = Button(screen, text="START", fg="white", bg="green",
                  command=lambda: start_button_click(int(entry_rounds.get()),
                                                     int(entry_cards.get()),
                                                     str(theme_var.get())))

welcome_text.pack(anchor=CENTER)
rounds_text.pack(anchor=CENTER)
entry_rounds.pack(anchor=CENTER)
cards_text.pack(anchor=CENTER)
entry_cards.pack(anchor=CENTER)
theme_text.pack(anchor=CENTER)
entry_theme.pack(anchor=CENTER)
click_me.pack(anchor=CENTER)

screen.mainloop()
