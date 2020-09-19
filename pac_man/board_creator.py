import pygame as pg
import PySimpleGUI as sg
from numpy import savetxt
from .classes import Board

def board_menu() -> int:
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


def board_draw(size):
    pg.init()
    screen = pg.display.set_mode((size, size))
    pg.display.set_caption("Board creator")
    clock = pg.time.Clock()
    board = Board(surface = screen)

    running = True
    while running:
        clock.tick(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                running = False
        board.display()
        pg.display.update()

    clock.tick(1)
    pg.quit()
    return board.pattern


def board_save(tab):
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


def board_main():
    size = board_menu()
    pattern = board_draw(size)
    error = board_save(pattern)

    if error: print("Not saved")
    else: print("Saved")

    return 0


if __name__ == '__main__':
    main()
