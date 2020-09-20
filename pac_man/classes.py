import pygame as pg
import random

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
        self.pattern = pattern    #plik lub tablica

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
    def __init__(self, x, y, color =  (175, 243, 98)):
        self.x = x
        self.y = y
        self.color = color

        # TODO: ugly, find `static` equivalent in python
        self.directions = {"LEFT": (-1,0), "RIGHT": (1,0),"UP": (0,-1), "DOWN": (0,1)}

    def display(self, board: Board):
        rectangle = pg.Rect((self.x*board.field_size, self.y*board.field_size), (board.field_size, board.field_size))
        pg.draw.rect(board.surface, (218, 247, 166), rectangle)

class Player(Character):
    # player move, when key is pressed
    def __init__(self, x, y, color =  (175, 243, 98)):
        super().__init__(x,y,color)
        self.left_key = pg.K_LEFT #, pg.K_a}
        self.right_key = pg.K_RIGHT #, pg.K_d}
        self.up_key = pg.K_UP #, pg.K_w}
        self.down_key = pg.K_DOWN #, pg.K_s}

    def move(self, key):

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

        self.x += direction[0]
        self.y += direction[1]

class Enemy(Character):
    # enemies move automatically

    # self.direction = random.choice(self.directions(keys))

    # def turn(self, turn_direcions):
    #     self.direction = turn_direcions

    def move(self, event, board_size):
        pass
        # TODO
        # head = self.positions[0]
        # new_head = [head[0] + self.direction[0], head[1] + self.direction[1]]
        #
        # # check if hiting the border
        # elif not(0 <= new_head[0] < board_size and  0 <= new_head[1] < board_size):
        #     if self.wall_die:
        #         raise GameOver
        #     else:
        #         if new_head[0] < 0: new_head[0] = board_size
        #         elif new_head[0] == board_size: new_head[0] = 0
        #         elif new_head[1] < 0: new_head[1] = board_size
        #         elif new_head[1] == board_size: new_head[1] = 0
        #
        # self.positions.insert(0, new_head)
