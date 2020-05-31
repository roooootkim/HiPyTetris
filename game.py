import tetris
import tetris_gym
import pygame as pg
from setting import *
successes, failures = pg.init()
print("{0} successes and {1} failures in game.py".format(successes, failures))


class Player:
    def __init__(self, pos, key_dic):
        self.game = tetris.Board()
        self.width = self.game.col * block_size
        self.height = self.game.row * block_size
        if pos == 'center':
            self.x = (size[0] - self.width) // 2
            self.y = (size[1] - self.height) // 2
        elif pos == 'right':
            self.x = (size[0] // 2 - self.width) // 2
            self.y = (size[1] - self.height) // 2
        elif pos == 'left':
            self.x = (size[0] // 2 - self.width) // 2 + size[0] // 2
            self.y = (size[1] - self.height) // 2
        else:
            print("pos 잘못넣음")
        self.speed = 3
        self.key_set = key_dic
        self.key_count = {'right': -1, 'left': -1, 'up': -1, 'down': -1, 'drop': -1}
        self.key_speed = {'right': FPS // 10, 'left': FPS // 10, 'up': FPS // 3, 'down': FPS // 15, 'drop': FPS // 2}
        self.fall_time = FPS

    def draw_board(self, screen):
        pg.draw.rect(screen, colors[0], [self.x, self.y, self.width, self.height])
        board = self.game.get_data()
        d_piece = self.game.get_dropped()
        d_shape = d_piece.shape[d_piece.rotation]
        for row in range(self.game.row):
            for col in range(self.game.col):
                if board[row][col] != 0:
                    pg.draw.rect(screen, colors[board[row][col]],
                                 [self.x + col * block_size, self.y + row * block_size, block_size, block_size])
        # 떨어질 모양을 예측해서 그려주는 반복문.
        for i in range(4):
            for j in range(4):
                if d_shape[i][j] != 0 and 0 <= d_piece.x + j < self.game.col and 0 <= d_piece.y + i < self.game.row:
                    if board[d_piece.y + i][d_piece.x + j] == 0:
                        pg.draw.circle(screen, colors[d_shape[i][j]],
                                       [self.x + (d_piece.x + j) * block_size + block_size // 2,
                                        self.y + (d_piece.y + i) * block_size + block_size // 2], block_size // 3)

    def key_input(self, event):
        if event.type == pg.KEYDOWN:
            for k in self.key_set.keys():
                if event.key == self.key_set[k]:
                    self.key_count[k] = self.key_speed[k]
        if event.type == pg.KEYUP:
            for k in self.key_set.keys():
                if event.key == self.key_set[k]:
                    self.key_count[k] = -1

    def move_piece(self):
        for k in self.key_set.keys():
            if self.key_count[k] != -1:
                if self.key_count[k] == self.key_speed[k]:
                    self.key_count[k] = 0
                    self.game.control(k)
                    if k == 'down' or k == 'drop':
                        self.fall_time = FPS
                else:
                    self.key_count[k] += 1

    def fall_time_check(self):
        self.fall_time -= self.speed
        if self.fall_time <= 0:
            self.fall_time = FPS
            self.game.control('down')

    def is_game_over(self):
        return self.game.game_over

    @staticmethod
    def make_multi(player1, player2):
        player1.game.take_enemy(player2.game)
        player2.game.take_enemy(player1.game)


class AI_Player:
    def __init__(self, pos):
        self.env = tetris_gym.TetrisEnv()
        self.game = self.env.game
        self.width = self.game.col * block_size
        self.height = self.game.row * block_size
        if pos == 'center':
            self.x = (size[0] - self.width) // 2
            self.y = (size[1] - self.height) // 2
        elif pos == 'right':
            self.x = (size[0] // 2 - self.width) // 2
            self.y = (size[1] - self.height) // 2
        elif pos == 'left':
            self.x = (size[0] // 2 - self.width) // 2 + size[0] // 2
            self.y = (size[1] - self.height) // 2

    def draw_board(self, screen):
        pg.draw.rect(screen, colors[0], [self.x, self.y, self.width, self.height])
        board = self.game.get_data()
        d_piece = self.game.get_dropped()
        d_shape = d_piece.shape[d_piece.rotation]
        for row in range(self.game.row):
            for col in range(self.game.col):
                if board[row][col] != 0:
                    pg.draw.rect(screen, colors[board[row][col]],
                                 [self.x + col * block_size, self.y + row * block_size, block_size, block_size])
        # 떨어질 모양을 예측해서 그려주는 반복문.
        for i in range(4):
            for j in range(4):
                if d_shape[i][j] != 0 and 0 <= d_piece.x + j < self.game.col and 0 <= d_piece.y + i < self.game.row:
                    if board[d_piece.y + i][d_piece.x + j] == 0:
                        pg.draw.circle(screen, colors[d_shape[i][j]],
                                       [self.x + (d_piece.x + j) * block_size + block_size // 2,
                                        self.y + (d_piece.y + i) * block_size + block_size // 2], block_size // 3)

    def is_game_over(self):
        return self.game.game_over
