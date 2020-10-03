"""
create game window, control game logic
"""

from numpy import loadtxt, ndarray
import pygame as pg
from .classes import *
from .language import *

def board_from_file(filename: str) -> (set, set, ndarray):
    filename = "boards/" + filename
    players_pos = set()
    enemies_pos = set()
    f=open(filename)
    line = f.readline().split()
    print("players", line)
    for pos in line:
        players_pos.add((int(pos.split(",")[0]), int(pos.split(",")[1])))
        print(players_pos)
    line = f.readline().split()
    print("enemies", line)
    for pos in line:
        enemies_pos.add((int(pos.split(",")[0]), int(pos.split(",")[1])))
        print(enemies_pos)
    f.close()
    pattern = loadtxt(fname=filename, delimiter=" ", skiprows=2, dtype=int)
    return (players_pos, enemies_pos, pattern)


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
    players_pos, enemies_pos, pattern = board_from_file(personalize['board'])
    print(players_pos, enemies_pos)
    screen_size = len(pattern)*pixel
    # TODO: choose enemies_quantity in settings
    enemies_quantity = 4;

    pg.init()
    screen = pg.display.set_mode((screen_size, screen_size))
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,1000' # sets window position – DOESN'T WORK

    pg.display.set_caption("Pac man")
    #icon = pg.image.load("pac_man/icon.png")
    # pg.display.set_icon(icon)

    clock = pg.time.Clock()

    board = Board(screen, pattern, pixel)
    center = int(board.sizeInFields/2)

    food = []
    for i in range(board.sizeInFields):
        for j in range(board.sizeInFields):
            if pattern[j][i] == 0:
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

    # # display 3...2...1...
    # font_big = pg.font.SysFont(None, 300)
    # #
    # for i in range(3,0,-1):
    # #     text = font_big.render(f"{i}", True, (0,0,0))
    #     display(board, players, enemies, food)
    # #     screen.blit(text, ((center*board.field_size)-50, (center*board.field_size)-80))
    #     pg.display.update()
    #     clock.tick(1)
    # #
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

            if not(paused):
                keys = pg.key.get_pressed()

                if enemies_round == 0:
                    for e in enemies: e.move(board.pattern, board.sizeInFields, [p.position for p in players], [e.position for e in enemies])
                    enemies_round = 1
                else: enemies_round -= 1

                for player in players:
                    food = player.move(keys, board.pattern, board.sizeInFields, food)
                    player.check_kill([e.position for e in enemies])

        except GameOver:
            running = False
        except GamePause:
            paused = not(paused)

        display(board, players, enemies, food)

        # show_score:
        #     text = font.render(lang['score'].format(score), True, (0,0,0))
        #     screen.blit(text, (10, 20))
        #     pg.display.update()

        if paused:  # TODO: unpause
            text = font.render(lang['pause'], True, (0,0,0))
            screen.blit(text, (screen_size-100, 20))
            pg.display.update()

    clock.tick(1)
    pg.quit()

    return [f'{(p.score/food_quantity*100):.2f}' for p in players]


if __name__ == '__main__':
    main()
