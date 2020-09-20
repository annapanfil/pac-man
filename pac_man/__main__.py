from os import listdir
from .gui import *
from .game import *
from .language import *
from .board_creator import board_main

def main():
    # default settings
    if 'personalize' not in locals(): personalize = {'lang': 'pl', 'board': listdir('./boards')[0], 'controls_p1': 'arrows', 'p2': False}
    lang = languages[personalize['lang']]

    choice = mainMenu(lang)

    while choice != 'exit':
        if choice == 'play':
            score = game(personalize)
            choice = exitMenu(score, personalize)

        elif choice == 'settings' :
            personalize = settings(personalize)
            lang = languages[personalize['lang']]
            choice = mainMenu(lang)

        elif choice == 'creator':
            board_main()
            choice = mainMenu(lang)

        elif choice == 'info':
            info(lang)
            choice = mainMenu(lang)


if __name__ == '__main__':
    main()
    # board_main()
