import tetris
import tetris_gym
import pygame as pg
from setting import *
successes, failures = pg.init()
print("{0} successes and {1} failures in game.py".format(successes, failures))


class Player:
    def __init__(self, pos, key_dic, waiting_state=False):
        self.game = tetris.Board()
        self.width = self.game.col * block_size
        self.height = self.game.row * block_size
        self.x, self.y, self.px, self.py, self.draw_next_piece = self.set_pos(pos)
        self.speed = 3
        self.key_set = key_dic
        self.key_count = {'right': -1, 'left': -1, 'up': -1, 'down': -1, 'drop': -1}
        self.key_speed = {'right': FPS // 10, 'left': FPS // 10, 'up': FPS // 3, 'down': FPS // 15, 'drop': FPS // 2}
        self.fall_time = FPS
        self.waiting_state = waiting_state
        self.attack_count = 0

    def set_pos(self, pos):
        self.draw_next_piece = True
        if pos == 'center':
            self.x = (size[0] - self.width) // 2
            self.y = (size[1] - self.height) // 2
            self.px = self.x - block_size * 5
            self.py = self.y + bezel
        elif pos == 'left':
            self.x = (size[0] // 2 - self.width) // 2 + block_size * 3
            self.y = (size[1] - self.height) // 2
            self.px = self.x - block_size * 5
            self.py = self.y + bezel
        elif pos == 'right':
            self.x = (size[0] // 2 - self.width) // 2 + size[0] // 2 - block_size * 3
            self.y = (size[1] - self.height) // 2
            self.px = self.x + self.width + block_size
            self.py = self.y + bezel

        return self.x, self.y, self.px, self.py, self.draw_next_piece

    def draw_board(self, screen):
        board = self.game.get_data()
        d_piece = self.game.get_dropped()
        d_shape = d_piece.shape[d_piece.rotation]
        next_shape = self.game.next_piece.shape[self.game.next_piece.rotation]

        pg.draw.rect(screen, colors[0], [self.x, self.y, self.width, self.height])

        if self.waiting_state:
            font = pg.font.SysFont("arial", 30, True, False)
            txt_surface = font.render("Player waiting...", True, colors[1])
            screen.blit(txt_surface, (self.x, self.y))
            return

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
        # next_piece 를 그려줌
        if self.draw_next_piece:
            pg.draw.rect(screen, colors[-1],
                         [self.px - bezel, self.py - bezel, block_size * 4 + bezel * 2, block_size * 4 + bezel * 2])
            for i in range(4):
                for j in range(4):
                    pg.draw.rect(screen, colors[next_shape[i][j]],
                                 [self.px + j * block_size, self.py + i * block_size, block_size, block_size])

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
            return self.game.control('down')
        return -1

    def is_game_over(self):
        return self.game.game_over

    def get_score(self):
        return self.game.line_score

    @staticmethod
    def make_multi(player1, player2):
        player1.game.take_enemy(player2.game)
        player2.game.take_enemy(player1.game)

    # ... method for online_play ... #
    def start_game(self):
        self.waiting_state = False

    def is_waiting(self):
        return self.waiting_state

    def cal_attack_count(self):
        self.attack_count += self.game.attack_stack

    def init_attack_count(self):
        self.attack_count = 0
        self.game.init_attack_stack()

    def check_attack_count(self):
        if self.attack_count != 0:
            return True
        else:
            return False

    def online_attacked(self, stack):
        self.game.attacked(stack)


class AI_Player(Player):
    def __init__(self, pos):
        Player.__init__(self, pos, {})
        self.env = tetris_gym.TetrisEnv()
        self.env.reset()
        self.game = self.env.game
        self.width = self.game.col * block_size
        self.height = self.game.row * block_size
        self.x, self.y, self.px, self.py, self.draw_next_piece = self.set_pos(pos)
        self.speed = 10
        self.find_col()

    def find_col(self):
        tmp = self.game.enemy
        self.game.enemy = None
        self.env.ai_step(True, False)
        self.game.enemy = tmp

    def fall_time_check(self):
        check = super(AI_Player, self).fall_time_check()
        if check != -1:
            self.find_col()

    def is_game_over(self):
        return self.game.game_over
