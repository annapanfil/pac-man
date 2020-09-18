from .gui import *
from .game import *
from .language import *

def main():
    # default settings
    if 'personalize' not in locals(): personalize = {'lang': 'pl', 'board_size': 480}
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

        elif choice == 'info':
            info(lang)
            choice = mainMenu(lang)


if __name__ == '__main__':
    main()
