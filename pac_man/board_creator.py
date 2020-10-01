"""allow user to draw new board and save it to text file"""

import pygame as pg
import PySimpleGUI as sg
from numpy import savetxt, zeros
from .classes import Board
from .language import *

def set_start_pos(board: Board, screen, clock) -> set:
    # create set of start positions (from user input)
    characters_pos = set()
    pixel = board.field_size
    while len(characters_pos) < 2:
        if pg.mouse.get_pressed()[0] == True:
            pos = pg.mouse.get_pos()
            if pos[0]<board.screen_size:              # board
                pos_in_pixels = (int(pos[0]/pixel), int(pos[1]/pixel))
                characters_pos.add(pos_in_pixels)
                print(characters_pos)


        board.display()
        for ch in characters_pos:
            pg.draw.rect(screen, (0,0,0), pg.Rect((ch[0]*pixel, ch[1]*pixel), (pixel, pixel)))

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                players_pos.add(None)
        clock.tick(100)

    clock.tick(1)

    return characters_pos


def board_menu() -> int:
    # show menu (choose board size)
    layout = [[sg.Text("Board size"), sg.Slider(range=(120, 1000), default_value=480,
                resolution = 40, orientation='horizontal', key="board_size")],
              [sg.Button("OK", key="-OK-")]]

    window = sg.Window("Board creator", layout, finalize=True, return_keyboard_events=True)

    while(True):
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return(values["board_size"])

        if event in ('\r', 'special 16777220', 'special 16777221'):
            elem = window.find_element_with_focus()
            if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:
                elem.Click()

        if event == "-OK-":
            window.Close()
            return int(values["board_size"])


def board_draw(size: int, lang: dict) -> (list, set):
    # allow user to draw the board and set positions of characters
    pg.init()
    pixel = 20
    screen = pg.display.set_mode((size+10*pixel, size))
    pg.display.set_caption("Board creator")
    clock = pg.time.Clock()
    board = Board(screen = screen, field_size = pixel, pattern = zeros((int(size/pixel), int(size/pixel)), dtype=int))
    dark_button = pg.Rect((size+2*pixel, int(size/2)-2*pixel), (pixel*2, pixel*2))
    light_button = pg.Rect((size+2*pixel, int(size/2)), (pixel*2, pixel*2))
    font = pg.font.SysFont(None, 30)

    msg = font.render(lang['s'].split("\n")[0], True, (0,0,255))
    msg_pos = (size + pixel, int(size/2)+4*pixel)
    msg2 = font.render(lang['s'].split("\n")[1], True, (0,0,255))
    msg2_pos = (size + pixel, int(size/2)+4*pixel+30)

    # DRAW BOARD
    screen.blit(msg, msg_pos)
    screen.blit(msg2, msg2_pos)
    running = True
    color = 1
    while running:
        if pg.mouse.get_pressed()[0] == True:
            pos = pg.mouse.get_pos()
            if pos[0]<size:              # board
                board.draw(pos, color)
            elif pos[0] >= size+2*pixel and pos[0] <= size+4*pixel:            # buttons
                if pos[1] >=  int(size/2)-2*pixel and pos[1] <= int(size/2):   # dark button
                    color = 1
                elif pos[1] >=  int(size/2) and pos[1] <= int(size/2)+2*pixel: # light button
                    color = 0

        clock.tick(1000)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                running = False

        board.display()
        pg.draw.rect(screen, board.dark_color, dark_button)
        pg.draw.rect(screen, board.light_color, light_button)
        pg.display.update()

    clock.tick(1)

    # SET CHARACTERS' START POSITION
    msg = font.render(lang['player_pos'].split("\n")[0], True, (0,0,255))
    msg2 = font.render(lang['player_pos'].split("\n")[1], True, (0,0,255))
    screen.blit(msg, msg_pos)
    screen.blit(msg2, msg2_pos)
    players_pos = set_start_pos(board, screen, clock)

    # TODO: enemies start position
    enemies_pos = set_start_pos(board, screen, clock)


    pg.quit()
    return (board.pattern, players_pos) if None not in (players_pos | enemies_pos) else []


def board_save(tab: list, players_pos: set) -> int:
    # save board to file, ask user for filename
    layout = [[sg.Text("Board name: "), sg.InputText(default_text="my_board", key="filename")],
              [sg.Button("Save", key="-OK-"), sg.Button("Cancel", key="-CANCEL-")]]

    window = sg.Window("Board creator", layout, finalize=True, return_keyboard_events=True)

    while(True):
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return 1

        if event in ('\r', 'special 16777220', 'special 16777221'):
            elem = window.find_element_with_focus()
            if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:
                elem.Click()

        if event == "-OK-":
            window.Close()
            f = (values["filename"])
            break

        if event == "-CANCEL-":
            window.close()
            return 1

    savetxt(f'boards/{f}', tab, fmt='%d', delimiter=' ', newline='\n')
    return 0


def board_main(language: dict):
    size = board_menu()
    pattern = board_draw(size, language)
    if pattern != []:
        error = board_save(*pattern)

        if error: print("Not saved")
        else: print("Saved")

    return 0


if __name__ == '__main__':
    main()
