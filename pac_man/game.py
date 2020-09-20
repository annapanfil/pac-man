from numpy import loadtxt
import pygame as pg
from .classes import *
from .language import *

def display(board, player, enemies):
    board.display()
    player.display(board)
    for e in enemies: e.display(board)

    pg.display.update()

def game(personalize):
    lang = languages[personalize['lang']]
    pixel = 20
    pattern = loadtxt(fname="boards/" + personalize['board'], delimiter=" ", skiprows=0, dtype=int)

    screen_size = len(pattern)*pixel
    enemies_quantity = 1;

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

    player = Player([center, center])
    enemies = [Enemy([1,1]) for i in range(enemies_quantity)]

    # display 3...2...1...
    # font_big = pg.font.SysFont(None, 300)
    #
    # for i in range(3,0,-1):
    #     text = font_big.render(f"{i}", True, (0,0,0))
    #     display(board, player, enemies)
    #     screen.blit(text, ((center*board.field_size)-50, (center*board.field_size)-80))
    #     pg.display.update()
    #     clock.tick(1)

    font = pg.font.SysFont(None, 30)

    # GAME LOOP
    running = True
    paused = False
    while running:
        clock.tick(10)
        # EVENTS HANDLING
        try:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                # elif event.type == pg.KEYDOWN:
                #     player.move(event)
            keys = pg.key.get_pressed()
            player.move(keys, board.pattern, board.sizeInFields)

            # if not(paused):
            #     for e in enemies: e.move(event, board.sizeInFields, food, speed_increase)

        except GameOver:
            running = False
        except GamePause:
            paused = not(paused)

        display(board, player, enemies)
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

    return 0

if __name__ == '__main__':
    main()
