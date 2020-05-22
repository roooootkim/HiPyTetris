import random
from copy import deepcopy

S = [[[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]],
     [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0]]]
Z = [[[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 2, 2], [0, 0, 0, 0]],
     [[0, 0, 0, 0], [0, 0, 2, 0], [0, 2, 2, 0], [0, 2, 0, 0]]]
I = [[[0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0]],
     [[0, 0, 0, 0], [3, 3, 3, 3], [0, 0, 0, 0], [0, 0, 0, 0]]]
O = [[[0, 0, 0, 0], [0, 4, 4, 0], [0, 4, 4, 0], [0, 0, 0, 0]]]
J = [[[0, 0, 0, 0], [0, 5, 0, 0], [0, 5, 5, 5], [0, 0, 0, 0]],
     [[0, 0, 5, 0], [0, 0, 5, 0], [0, 5, 5, 0], [0, 0, 0, 0]],
     [[0, 0, 0, 0], [0, 5, 5, 5], [0, 0, 0, 5], [0, 0, 0, 0]],
     [[0, 0, 5, 5], [0, 0, 5, 0], [0, 0, 5, 0], [0, 0, 0, 0]]]
L = [[[0, 0, 0, 0], [0, 0, 6, 0], [6, 6, 6, 0], [0, 0, 0, 0]],
     [[0, 6, 6, 0], [0, 0, 6, 0], [0, 0, 6, 0], [0, 0, 0, 0]],
     [[0, 0, 0, 0], [6, 6, 6, 0], [6, 0, 0, 0], [0, 0, 0, 0]],
     [[0, 6, 0, 0], [0, 6, 0, 0], [0, 6, 6, 0], [0, 0, 0, 0]]]
T = [[[0, 0, 0, 0], [0, 7, 7, 7], [0, 0, 7, 0], [0, 0, 0, 0]],
     [[0, 0, 0, 0], [0, 7, 0, 0], [0, 7, 7, 0], [0, 7, 0, 0]],
     [[0, 0, 0, 0], [0, 0, 7, 0], [0, 7, 7, 7], [0, 0, 0, 0]],
     [[0, 0, 0, 0], [0, 0, 7, 0], [0, 7, 7, 0], [0, 0, 7, 0]]]

shapes = [S, Z, I, O, J, L, T]

check_dir = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, -1), (1, 1), (-1, 1)]


class Piece:
    def __init__(self, row, column, shape, rotation=0):
        self.x = column
        self.y = row
        self.shape = shape
        self.rotation = rotation

    def rotate(self, dx=0, dy=0):
        self.rotation = (self.rotation + 1) % len(self.shape)
        self.x += dx
        self.y += dy

    def descend(self, dy=1):
        self.y += dy

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def move_up(self, dy):
        self.y -= dy


class Board:
    def __init__(self, row=20, column=10):
        self.row = row
        self.col = column
        self.grid = [[0 for col in range(column)] for row in range(row)]
        self.next_piece = self.get_piece()
        self.cur_piece = self.get_piece()
        self.enemy = None
        self.game_over = False

    def get_piece(self):
        return Piece(-3, int(self.col / 2 - 2), random.choice(shapes))

    def valid_space(self, x, y, shape, rotation):
        for i in range(4):
            for j in range(4):
                if shape[rotation][i][j] != 0:
                    if not(y + i < self.row and 0 <= x + j < self.col):
                        return False
                    elif y + i < 0:
                        pass
                    elif self.grid[y + i][x + j] != 0:
                        return False
        return True

    def drop_check(self):
        for dy in range(1, self.row * 2):
            if not self.valid_space(self.cur_piece.x, self.cur_piece.y + dy,
                                    self.cur_piece.shape, self.cur_piece.rotation):
                return dy - 1
        return 0

    def get_dropped(self):
        ret_piece = deepcopy(self.cur_piece)
        ret_piece.descend(self.drop_check())
        return ret_piece

    def is_game_over(self):
        for i in range(4):
            if self.cur_piece.y + i < 0 and self.cur_piece.shape[self.cur_piece.rotation][i].count(0) != 4:
                self.game_over = True
                return

    def control(self, key):
        if key == 'right':
            if self.valid_space(self.cur_piece.x + 1, self.cur_piece.y, self.cur_piece.shape, self.cur_piece.rotation):
                self.cur_piece.move_right()
        elif key == 'left':
            if self.valid_space(self.cur_piece.x - 1, self.cur_piece.y, self.cur_piece.shape, self.cur_piece.rotation):
                self.cur_piece.move_left()
        elif key == 'up':
            if self.valid_space(self.cur_piece.x, self.cur_piece.y, self.cur_piece.shape,
                                (self.cur_piece.rotation + 1) % len(self.cur_piece.shape)):
                self.cur_piece.rotate()
            else:
                for i in range(10):
                    for (dx, dy) in check_dir:
                        if self.valid_space(self.cur_piece.x + i * dx, self.cur_piece.y + i * dy, self.cur_piece.shape,
                                            (self.cur_piece.rotation + 1) % len(self.cur_piece.shape)):
                            self.cur_piece.rotate(i * dx, i * dy)
                            return
        elif key == 'down':
            if self.valid_space(self.cur_piece.x, self.cur_piece.y + 1, self.cur_piece.shape, self.cur_piece.rotation):
                self.cur_piece.descend()
            else:
                self.update_grid()
        elif key == 'drop':
            self.cur_piece.descend(self.drop_check())
            return self.update_grid()

    def get_data(self):
        ret_grid = deepcopy(self.grid)

        cur_x = self.cur_piece.x
        cur_y = self.cur_piece.y
        cur_shape = self.cur_piece.shape[self.cur_piece.rotation]
        for i in range(4):
            for j in range(4):
                if cur_shape[i][j] != 0 and 0 <= cur_x + j < self.col and 0 <= cur_y + i < self.row:
                    ret_grid[cur_y + i][cur_x + j] = cur_shape[i][j]
        return ret_grid

    def update_grid(self):
        # 게임오버인지 체크하여 self.game_over 변수를 업데이트.
        self.is_game_over()

        # grid 업데이트
        self.grid = self.get_data()
        self.cur_piece = self.next_piece
        self.next_piece = self.get_piece()

        # 줄 차있으면 삭제
        attack_stack = 0
        for r in range(self.row):
            if self.grid[r].count(0) == 0:
                del self.grid[r]
                self.grid.insert(0, [0 for col in range(self.col)])
                attack_stack += 1
        if self.enemy is not None:
            self.attack(self.enemy, attack_stack)
        return attack_stack

    def take_enemy(self, player):
        self.enemy = player

    @staticmethod
    def attack(enemy, stack):
        enemy.attacked(stack)

    def attacked(self, stack):
        attack_row = [8 for col in range(self.col)]
        attack_row[random.randrange(self.col)] = 0
        for i in range(stack):
            if self.grid[i].count(0) == self.col:
                del self.grid[i]
                self.grid.insert(self.row - 1, attack_row)
            else:
                print("여기서 게임 오버 시켜야해")

        if not self.valid_space(self.cur_piece.x, self.cur_piece.y, self.cur_piece.shape, self.cur_piece.rotation):
            self.cur_piece.move_up(stack)
