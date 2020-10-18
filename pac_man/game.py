"""
create game window, control game logic
"""
# IDEA: change players, enemies and food from lists to sets

import pygame as pg
from .classes import *
from .language import *

def display(board: Board, players: list, enemies: list, food:list) -> None:
    board.display()
    for f in food: f.display(board)
    for p in players: p.display(board)
    for e in enemies: e.display(board)

    pg.display.update()


def game(personalize: dict) -> [int, int]:
    # INITIALIZE
    lang = languages[personalize['lang']]
    pixel = 20
    enemies_quantity = 4;  # TODO: choose enemies_quantity in settings

    board = Board()
    players_pos, enemies_pos = board.from_file(personalize['board'])
    screen_size = len(board.pattern)*board.field_size

    pg.init()
    screen = pg.display.set_mode((screen_size, screen_size))
    board.set_screen(screen)
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,1000' # sets window position – DOESN'T WORK
    pg.display.set_caption("Pac man")
    #icon = pg.image.load("pac_man/icon.png")
    # pg.display.set_icon(icon)
    clock = pg.time.Clock()

    food = []
    for i in range(board.sizeInFields):
        for j in range(board.sizeInFields):
            if board.pattern[j][i] == 0:
                food.append(Food((i, j)))
    food_quantity = len(food)

    controls = (pg.K_a, pg.K_d, pg.K_w, pg.K_s) if personalize['controls_p1'] == 'adws' else (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN)
    image = pg.image.load('graphics/player.png')
    image = pg.transform.scale(image, (pixel, pixel))
    players = [Player(players_pos.pop(), controls, image = image)]
    if personalize['p2']:
        controls = (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN) if personalize['controls_p1'] == 'adws' else (pg.K_a, pg.K_d, pg.K_w, pg.K_s)
        players.append(Player(players_pos.pop(), controls, image=image))

    image = pg.image.load('graphics/enemy.png')
    image = pg.transform.scale(image, (pixel, pixel))
    enemies = [Enemy(enemies_pos.pop(), [p.position for p in players], image=image) for i in range(enemies_quantity)]

    # display 3...2...1...
    font_big = pg.font.SysFont(None, 300)
    for i in range(3,0,-1):
        text = font_big.render(f"{i}", True, (0,0,0))
        display(board, players, enemies, food)
        screen.blit(text, ((int(board.sizeInFields/2)*board.field_size-50), (int(board.sizeInFields/2)*board.field_size-80)))
        pg.display.update()
        clock.tick(1)

    font = pg.font.SysFont(None, 30)

    # GAME LOOP
    running = True
    paused = False
    enemies_round = 0
    while running:
        clock.tick(10)
        # EVENTS HANDLING
        try:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN and event.key in {ord('p'), ord(' ')}:
                    paused = not(paused)

            if not(paused):
                keys = pg.key.get_pressed()

                if enemies_round == 0:
                    for e in enemies: e.move(board.pattern, [p.position for p in players], [e.position for e in enemies])
                    enemies_round = 1
                else: enemies_round -= 1

                for player in players:
                    food = player.move(keys, board.pattern, food)
                    player.check_kill([e.position for e in enemies])

                display(board, players, enemies, food)

            if paused:
                text = font.render(lang['pause'], True, (0,0,0))
                screen.blit(text, (screen_size-100, 20))
                pg.display.update()

        except GameOver:
            running = False

        # show_score:
        #     text = font.render(lang['score'].format(score), True, (0,0,0))
        #     screen.blit(text, (10, 20))
        #     pg.display.update()

    clock.tick(1)
    pg.quit()

    return [f'{(p.score/food_quantity*100):.2f}' for p in players]


if __name__ == '__main__':
    main()
