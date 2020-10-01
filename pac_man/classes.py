"""
player, enemy, board and food classes (including methods for displaying, movement and )
"""

import pygame as pg
import random
import pdb

# TODO: różne obrazki dla różnych graczy

# TODO: oddziaływanie gracz-gracz

# TODO: przechwytywanie pauzy

# QUESTION: czy przeciwnik ma używać teleportu?


class GameOver(Exception):
    pass

class GamePause(Exception):
    pass

class Board():
    def __init__(self, screen, pattern, field_size = 20, light_color=(98, 175, 243), dark_color=(98, 102, 243)):
        self.field_size = field_size     # pixel
        self.screen = screen             # pygame surface
        self.light_color = light_color
        self.dark_color = dark_color
        self.pattern = pattern           # numpy array

    @property
    def sizeInFields(self):
        return int(self.screen_size/self.field_size)

    @property
    def screen_size(self):
        return self.screen.get_width()


    def display(self):
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[i])):
                rectangle = pg.Rect((i*self.field_size, j*self.field_size), (self.field_size, self.field_size))
                if self.pattern[j][i]==1:
                    pg.draw.rect(self.screen, self.dark_color, rectangle)
                else:
                    pg.draw.rect(self.screen, self.light_color, rectangle)

    def draw(self, position: tuple, color = 1):
        ### change board pattern ###
        x = int(position[0]/self.field_size)
        y = int(position[1]/self.field_size)
        # print(position, x, y)
        self.pattern[y][x] = color

class Character():
    def __init__(self, position: list, color = (175, 243, 98), image = None):
        self.position = position
        self.color = color
        self.org_image = image
        self.image = image

    def display(self, board: Board):
        if self.image != None:
            board.screen.blit(self.image, (self.position[0]*board.field_size, self.position[1]*board.field_size))
        else:
            print(self.image)
            rectangle = pg.Rect((self.position[0]*board.field_size, self.position[1]*board.field_size), (board.field_size, board.field_size))
            pg.draw.rect(board.screen, self.color, rectangle)

    def valid_move(self, turn: list, pattern: list, board_size: int) -> tuple:
        ### check if move is valid ###
        new_pos = [self.position[0] + turn[0], self.position[1] + turn[1]]

        # hit the border – teleport
        if new_pos[0] < 0: new_pos[0] = board_size-1
        elif new_pos[0] == board_size: new_pos[0] = 0
        elif new_pos[1] < 0: new_pos[1] = board_size-1
        elif new_pos[1] == board_size: new_pos[1] = 0

        # hit the wall
        elif pattern[new_pos[1]][new_pos[0]] == 1:
            return False

        return new_pos

    def check_kill(self, enemies_pos):
        for e in enemies_pos:
            if self.position == e:
                raise GameOver

class Player(Character):
    def __init__(self, position: list, controls: tuple, color = (218, 247, 16), image = None):
        super().__init__(position, color, image)
        self.left_key = controls[0]
        self.right_key = controls[1]
        self.up_key = controls[2]
        self.down_key = controls[3]
        self.score = 0

    def move(self, key, pattern, board_size, food):
        ### move when key is pressed (if valid)###
        image = None
        direction = [0,0]

        if key[self.right_key]:
            direction[0] += 1
            image = self.org_image.copy()

        if key[self.left_key]:
            direction[0] -= 1
            image = pg.transform.flip(self.org_image, True, False) # y-axes

        if key[self.up_key]:
            direction[1] -= 1
            if direction[0] != 0: image = pg.transform.rotate(image,45*direction[0]) # diagonally
            else: image = pg.transform.rotate(self.org_image, 90) # up

        if key[self.down_key]:
            direction[1] += 1
            if direction[0] != 0: image = pg.transform.rotate(image,-45*direction[0]) # diagonally
            else: image = pg.transform.rotate(self.org_image, -90) # down

        if key[pg.K_p] or key[pg.K_SPACE]:
            raise GamePause

        if image != None: self.image = image
        new_pos = self.valid_move(direction, pattern, board_size)

        if new_pos != False:  # if cannot move, stay
            self.position = new_pos

            # check if eating food
            for i in range(len(food)):
                if tuple(new_pos) == food[i].position:
                    food[i].eat(self, board_size)
                    food.pop(i)
                    break

        return food

class Enemy(Character):
    def __init__(self, position, players_pos, color = (243, 98, 102), image=None):
        super().__init__(position, color, image)
        self.prev_position = self.position
        self.prev_turn = [0,1]

    def turn(self, players_pos):
        # choose the nearest player
        player = players_pos[0]
        for p in players_pos[1:]:
            if p[0]**2+p[1]**2 < player[0]**2+player[1]**2:
                player = p

        turn=[0,0]
        # go to the player
        for i in range(2):
            x = self.position[i] - player[i]
            if x<0: turn[i] = 1
            elif x>0: turn[i]= -1

        return turn


    def valid_move(self, turn: list, pattern: list, board_size: int, enemies_pos:list) -> tuple:
        new_pos = Character.valid_move(self, turn, pattern, board_size)

        # check if not going back
        if new_pos == self.prev_position:
            return False


        # check if not on other enemy:
        for e in enemies_pos:
            if new_pos == e:
                return False

        return new_pos

    def plusMinus1(self, turn, index, pattern, board_size, enemies_pos):
        ### try +-1 on position index ###
        for val in {-1, 1}:
            turn[index] = val
            new_pos = self.valid_move(turn, pattern, board_size, enemies_pos)

            if new_pos != False:
                return (new_pos, turn)

        return False

    def checkValue(self, turn, val, pattern, board_size, enemies_pos):
        ### try multiplication by val on both positions in turn ###
        for i in range(2):
            temp_turn = turn.copy()
            temp_turn[i] *= val
            new_pos = self.valid_move(temp_turn, pattern, board_size,enemies_pos)

            if new_pos != False:
                return (new_pos,  temp_turn)

        return False


    def move(self, pattern, board_size, players_pos, enemies_pos):
        ### move automatically ###
        # TODO: zdarza mu się chodzić w kółko

        turn = self.turn(players_pos)
        new_pos = self.valid_move(turn, pattern, board_size, enemies_pos)

        if new_pos == False:  # if cannot move, choose other place
            # continue movement
            new_pos = self.valid_move(self.prev_turn, pattern, board_size, enemies_pos)

            if new_pos != False:
                turn = self.prev_turn

            else:
                # check other options
                if turn[0]*turn[1]==0:              # N, S, E or W
                    # assume W
                    index = 0 if turn[0] == 0 else 1
                    iterator = -1 * turn[not(index)]
                    for _ in range(2):     # try diagonally and everything but opposite
                        # first, try NW and SW
                        # if not, try N and S
                        # if not, try NE and SE

                        temp = self.plusMinus1(turn, index, pattern, board_size, enemies_pos)
                        if temp != False:
                            new_pos = temp[0]
                            turn = temp[1]
                            break
                        turn[not(index)] += iterator

                else:                        # diagonally
                    # assume  NW
                    for val in [0,-1]:
                        # try N and W
                        # if not, try NE and SW

                        temp = self.checkValue(turn, val, pattern, board_size, enemies_pos)

                        if temp != False:
                            new_pos = temp[0]
                            turn = temp[1]
                            break

                    if new_pos == False:
                        # if not, try E and S

                        temp = self.checkValue([-x for x in turn], 0, pattern, board_size, enemies_pos)
                        if temp != False:
                            new_pos = temp[0]
                            turn = temp[1]

                if new_pos == False:
                    # E / SE
                    turn = [-x for x in turn]   # opposite direction
                    new_pos = self.valid_move(turn, pattern, board_size, enemies_pos)

                    if new_pos == False:    # trapped
                        new_pos = self.prev_position
                        turn = [-x for x in self.prev_turn]

        self.prev_turn = turn
        self.prev_position = self.position
        self.position = new_pos

class Food():
    def __init__(self, position: tuple):
        self.position = position
        self.color = (243, 166, 98)

    def display(self, board):
        field = board.field_size
        circle_center = (int(self.position[0]*field + field/2), int(self.position[1]*field + field/2))
        pg.draw.circle(board.screen, self.color, circle_center, int(field/4))

    def eat(self, player, board_size):
        player.score += 1
        del(self)
