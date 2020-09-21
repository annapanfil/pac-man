import pygame as pg
import random
import pdb

class GameOver(Exception):
    def __init__(self, *args, **kwargs):
        super(GameOver, self).__init__(*args, **kwargs)

class GamePause(Exception):
    def __init__(self, *args, **kwargs):
        super(GamePause, self).__init__(*args, **kwargs)

class Board():
    def __init__(self, surface, pattern, field_size = 20, light_color=(98, 175, 243), dark_color=(98, 102, 243)):
        self.field_size = field_size
        self.surface = surface
        self.light_color = light_color
        self.dark_color = dark_color
        self.pattern = pattern    #tablica

    @property
    def sizeInFields(self):
        return int(self.screen_size/self.field_size)

    @property
    def screen_size(self):
        return self.surface.get_width()


    def display(self):
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[i])):
                rectangle = pg.Rect((i*self.field_size, j*self.field_size), (self.field_size, self.field_size))
                if self.pattern[j][i]==1:
                    pg.draw.rect(self.surface, self.dark_color, rectangle)
                else:
                    pg.draw.rect(self.surface, self.light_color, rectangle)

    def draw(self, position: tuple, color = 1):
        x = int(position[0]/self.field_size)
        y = int(position[1]/self.field_size)
        # print(position, x, y)
        self.pattern[y][x] = color

class Character():
    def __init__(self, position: list, color = (175, 243, 98)):
        self.position = position
        self.color = color

    def display(self, board: Board):
        rectangle = pg.Rect((self.position[0]*board.field_size, self.position[1]*board.field_size), (board.field_size, board.field_size))
        pg.draw.rect(board.surface, self.color, rectangle)

    def valid_move(self, new_pos: list, pattern: list, board_size: int) -> tuple:

        # hit the border – teleport
        # note: enemies can teleport, they just dont want to
        if new_pos[0] < 0: new_pos[0] = board_size
        elif new_pos[0] == board_size: new_pos[0] = 0
        elif new_pos[1] < 0: new_pos[1] = board_size
        elif new_pos[1] == board_size: new_pos[1] = 0

        # hit the wall
        elif pattern[new_pos[1]][new_pos[0]] == 1:
            return [-100,-100]

        return new_pos

class Player(Character):
    # player move, when key is pressed
    def __init__(self, position: list, controls: tuple, color = (218, 247, 16)):
        super().__init__(position, color)
        self.left_key = controls[0]
        self.right_key = controls[1]
        self.up_key = controls[2]
        self.down_key = controls[3]

    def move(self, key, pattern, size):
        direction = (0,0)

        if key[self.left_key]:
            direction = (-1,0)
        elif key[self.right_key]:
            direction = (1,0)
        elif key[self.up_key]:
            direction = (0,-1)
        elif key[self.down_key]:
            direction = (0,1)
        elif key[pg.K_p] or key[pg.K_SPACE]:
            raise GamePause

        new_pos = [self.position[0]+direction[0], self.position[1]+direction[1]]

        new_pos = self.valid_move(new_pos, pattern, size)
        if new_pos != [-100,-100]:  # if cannot move, stay
            self.position = new_pos


class Enemy(Character):
    def turn(self, players_pos):
        player = players_pos[0] # TODO: choose nearest player
        turn=[0,0]

        # go to the player
        for i in range(2):
            x = self.position[i] - player[i]
            if x<0: turn[i]= 1
            elif x>0:
                turn[i]= -1

        new_pos = [self.position[0] + turn[0], self.position[1] + turn[1]]

        return new_pos

    # enemies move automatically
    def __init__(self, position, players_pos, color = (243, 98, 102)):
        super().__init__(position, color)
        self.direction = self.turn(players_pos)


    def move(self, event, pattern, board_size, players_pos):
        new_pos = self.turn(players_pos)
        new_pos = self.valid_move(new_pos, pattern, board_size)
        # pdb.set_trace()
        if new_pos != [-100,-100]:  # if cannot move, stay # TODO: choose other place
            self.position = new_pos
        else: print("invalid move")
