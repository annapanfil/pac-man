from numpy import loadtxt
import pygame as pg
from .classes import *
from .language import *

def display(board, players, enemies, food):
    board.display()
    for f in food: f.display(board)
    for p in players: p.display(board)
    for e in enemies: e.display(board)

    pg.display.update()

def game(personalize):
    lang = languages[personalize['lang']]
    pixel = 20
    pattern = loadtxt(fname="boards/" + personalize['board'], delimiter=" ", skiprows=0, dtype=int)

    screen_size = len(pattern)*pixel
    enemies_quantity = 0;

    # INITIALIZE PYGAME AND CREATE THE WINDOW
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
    players = [Player([center-3, 20], controls, image = image)]
    if personalize['p2']:
        controls = (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN) if personalize['controls_p1'] == 'adws' else (pg.K_a, pg.K_d, pg.K_w, pg.K_s)
        players.append(Player([center+1, center], controls), image=image)
        players[0].position[0]-= 1

    image = pg.image.load('graphics/enemy.png')
    image = pg.transform.scale(image, (pixel, pixel))
    enemies = [Enemy([center-1,2*i], [p.position for p in players], image=image) for i in range(enemies_quantity)]

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

        # if show_score:
        #     text = font.render(lang['score'].format(score), True, (0,0,0))
        #     screen.blit(text, (10, 20))
        #     pg.display.update()

        if paused:
            text = font.render(lang['pause'], True, (0,0,0))
            screen.blit(text, (screen_size-100, 20))
            pg.display.update()

    clock.tick(1)
    pg.quit()

    return [f'{(p.score/food_quantity*100):.0f}' for p in players]


if __name__ == '__main__':
    main()
