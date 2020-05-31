import tetris
import random
from copy import deepcopy


class TetrisEnv:
    def __init__(self):
        self.game = None
        self.observation = None
        self.reset()
        self.rot_action = [0, 1, 2, 3]
        self.col_action = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]

    # FLATTEN 때문에 수정해도 될듯
    def ob_update(self):
        self.observation = []
        for row in range(self.game.row):
            for col in range(self.game.col):
                if self.game.grid[row][col] != 0:
                    self.observation.append(1)
                else:
                    self.observation.append(0)

    def reset(self):
        self.game = tetris.Board()
        self.ob_update()

        return self.observation

    def rand_act(self):
        return [self.rot_action[random.randrange(0, 4)], self.col_action[random.randrange(0, 11)]]

    def step(self, action, do=False):
        height, lines, holes, bumpiness = 0, 0, 0, 0
        over = 0
        prev_g = deepcopy(self.game.grid)
        prev_p = deepcopy(self.game.cur_piece)
        prev_np = deepcopy(self.game.next_piece)
        while action[0] >= len(self.game.cur_piece.shape):
            action[0] %= len(self.game.cur_piece.shape)

        for i in [0, 1, -1, 2, -2]:
            if self.game.valid_space(action[1] + i, -4, self.game.cur_piece.shape, action[0]):
                action[1] += i
                break
        self.game.cur_piece.rotation = action[0]
        self.game.cur_piece.x = action[1]
        self.game.cur_piece.y = -4
        lines = self.game.control('drop')

        tmp_height = [0 for col in range(self.game.col)]
        for col in range(self.game.col):
            flag = False
            for row in range(self.game.row):
                if self.game.grid[row][col] != 0 and not flag:
                    tmp_height[col] = (self.game.row - row)
                    flag = True
                elif self.game.grid[row][col] == 0 and flag:
                    holes += 1
            height += tmp_height[col]
            if col != 0:
                bumpiness += abs(tmp_height[col - 1] - tmp_height[col])
        self.ob_update()

        if self.game.game_over:
            over = 1

        if not do:
            self.game.grid = prev_g
            self.game.cur_piece = prev_p
            self.game.next_piece = prev_np
            self.game.game_over = False

        return -0.51 * height + 0.76 * lines + -0.36 * holes + -0.18 * bumpiness + -100 * over
        # return self.observation, -0.51 * height + 0.76 * lines + -0.36 * holes + -0.18 * bumpiness, self.game.game_over

    def ai_step(self):
        rl = []
        opt = float('-inf')
        opt_a = [-1, -1]
        for s in range(0, 4):
            for c in range(0, 11):
                tmp = self.step([self.rot_action[s], self.col_action[c]])
                rl.append(tmp)
                if tmp >= opt:
                    opt = tmp
                    opt_a[0] = s
                    opt_a[1] = c
        self.step([self.rot_action[opt_a[0]], self.col_action[opt_a[1]]], True)
        return self.game.game_over


if __name__ == "__main__":
    game = TetrisEnv()
    game.reset()
    step_cnt = 0
    while not game.ai_step():
        step_cnt += 1
        if step_cnt % 100 == 0:
            print('step : ', step_cnt)

    print('done, step : ', step_cnt)
