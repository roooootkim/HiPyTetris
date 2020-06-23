import tetris
import random
import matplotlib.pylab as plt
from copy import deepcopy

'''
Tetris_gym.py
작성자 : 김근호

테트리스 ai 플레이를 위해 작성 된 모듈입니다.
테트리스 게임을 플레이하여 가장 높은 reward를 반환하는 action을 구해서 행동합니다.

이 모듈을 main으로 실행할 경우 matplotlib 패키지를 통해 10번의 게임 결과 ai의 생존 길이를 표로 출력합니다.
'''
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

    def step(self, action, do=False, drop=True):
        height, lines, holes, bumpiness, over = 0, 0, 0, 0, self.game.game_over
        cur_action = deepcopy(action)
        cur_grid = deepcopy(self.game.grid)
        cur_piece = deepcopy(self.game.cur_piece)
        cur_next_piece = deepcopy(self.game.next_piece)
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

        next_grid = deepcopy(self.game.grid)
        over = self.game.game_over

        if not do:
            self.game.grid = cur_grid
            self.game.cur_piece = cur_piece
            self.game.next_piece = cur_next_piece
            self.game.game_over = False

        if do and not drop:
            self.game.grid = cur_grid
            self.game.cur_piece = cur_piece
            self.game.cur_piece.rotation = action[0]
            self.game.cur_piece.x = action[1]
            self.game.cur_piece.y = -4
            self.game.next_piece = cur_next_piece
            self.game.game_over = False

        reward = -0.510066 * height + 0.760666 * lines + -0.35663 * holes + -0.184483 * bumpiness + -100 * over
        return cur_grid, cur_action, reward, next_grid, self.game.game_over

    def ai_step(self, do=True, drop=True):
        rl = []
        opt = float('-inf')
        opt_a = [-1, -1]
        for s in range(0, 4):
            for c in range(0, 11):
                _, _, tmp, _, _ = self.step([self.rot_action[s], self.col_action[c]])
                rl.append(tmp)
                if tmp >= opt:
                    opt = tmp
                    opt_a[0] = s
                    opt_a[1] = c
        self.step([self.rot_action[opt_a[0]], self.col_action[opt_a[1]]], do, drop)
        return self.game.game_over


if __name__ == "__main__":
    length_list = []
    avg = 0
    num = 10
    for i in range(num):
        game = TetrisEnv()
        game.reset()
        step_cnt = 0
        while not game.ai_step():
            step_cnt += 1
        length_list.append(step_cnt)
        avg += step_cnt
        print('(', i + 1, '/', num, ') -> step : ', step_cnt)
    avg /= num
    print('average : ', avg)

    plt.title("Heuristics Algorithm")
    plt.plot(length_list)
    plt.show()
