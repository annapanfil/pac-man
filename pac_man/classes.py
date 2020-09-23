import pygame as pg
import random
import pdb

# TODO: obrazki

# TODO: oddziaływanie obiekt-obiekt
## gracz-gracz

# QUESTION: czy przeciwnik ma używać teleportu?


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

    def valid_move(self, turn: list, pattern: list, board_size: int) -> tuple:
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
    # player move, when key is pressed
    def __init__(self, position: list, controls: tuple, color = (218, 247, 16)):
        super().__init__(position, color)
        self.left_key = controls[0]
        self.right_key = controls[1]
        self.up_key = controls[2]
        self.down_key = controls[3]
        self.score = 0

    def move(self, key, pattern, board_size, food):

        direction = [0,0]

        if key[self.left_key]:
            direction[0] -= 1
        if key[self.right_key]:
            direction[0] += 1
        if key[self.up_key]:
            direction[1] -= 1
        if key[self.down_key]:
            direction[1] += 1
        if key[pg.K_p] or key[pg.K_SPACE]:
            raise GamePause

        new_pos = self.valid_move(direction, pattern, board_size)
        if new_pos != False:  # if cannot move, stay
            self.position = new_pos

            for i in range(len(food)):
                if tuple(new_pos) == food[i].position:
                    food[i].eat(self, board_size)
                    food.pop(i)
                    break

        return food


class Enemy(Character):
    # enemies move automatically
    def __init__(self, position, players_pos, color = (243, 98, 102)):
        super().__init__(position, color)
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
        # try +-1 on position index
        for val in {-1, 1}:
            turn[index] = val
            new_pos = self.valid_move(turn, pattern, board_size, enemies_pos)
            
            if new_pos != False:
                return (new_pos, turn)

        return False


    def checkValue(self, turn, val, pattern, board_size, enemies_pos):
        for i in range(2):
            temp_turn = turn.copy()
            temp_turn[i] *= val
            new_pos = self.valid_move(temp_turn, pattern, board_size,enemies_pos)

            if new_pos != False:
                return (new_pos,  temp_turn)

        return False


    def move(self, pattern, board_size, players_pos, enemies_pos):
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
        rectangle = pg.Rect((self.position[0]*board.field_size, self.position[1]*board.field_size), (board.field_size, board.field_size))
        pg.draw.rect(board.surface, self.color, rectangle)

    def eat(self, player, board_size):
        player.score += 1
        del(self)
