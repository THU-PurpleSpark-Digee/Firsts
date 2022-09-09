import random

from getaround import _get_around as _get_around
from mine import Mine, BlockStatus

BLOCK_WIDTH = 30
BLOCK_HEIGHT = 16
SIZE = 42  # 块大小
MINE_COUNT = 99  # 地雷数


class MineBlock:
    def __init__(self):
        self._block = [[Mine(i, j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]

        # 埋雷
        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), MINE_COUNT):
            self._block[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1

    def get_block(self):
        return self._block

    block = property(fget=get_block)

    def getmine(self, x, y):
        return self._block[y][x]

    def open_mine(self, x, y):
        # 踩到雷了
        if self._block[y][x].value:
            self._block[y][x].status = BlockStatus.bomb
            return False

        # 先把状态改为 opened
        self._block[y][x].status = BlockStatus.opened

        around = _get_around(x, y)

        _sum = 0
        for i, j in around:
            if self._block[j][i].value:
                _sum += 1
        self._block[y][x].around_mine_count = _sum

        # 如果周围没有雷，那么将周围8个未中未点开的递归算一遍
        # 这就能实现一点出现一大片打开的效果了
        if _sum == 0:
            for i, j in around:
                if self._block[j][i].around_mine_count == -1:
                    self.open_mine(i, j)

        return True

    def double_mouse_button_down(self, x, y):
        if self._block[y][x].around_mine_count == 0:
            return True

        self._block[y][x].status = BlockStatus.double

        around = _get_around(x, y)

        sumflag = 0  # 周围被标记的雷数量
        for i, j in _get_around(x, y):
            if self._block[j][i].status == BlockStatus.flag:
                sumflag += 1
        # 周边的雷已经全部被标记
        result = True
        if sumflag == self._block[y][x].around_mine_count:
            for i, j in around:
                if self._block[j][i].status == BlockStatus.normal:
                    if not self.open_mine(i, j):
                        result = False
        else:
            for i, j in around:
                if self._block[j][i].status == BlockStatus.normal:
                    self._block[j][i].status = BlockStatus.hint
        return result

    def double_mouse_button_up(self, x, y):
        self._block[y][x].status = BlockStatus.opened

        for i, j in _get_around(x, y):
            if self._block[j][i].status == BlockStatus.hint:
                self._block[j][i].status = BlockStatus.normal


if __name__ == '__main__':
    mineblock1 = MineBlock()
    print(mineblock1)
    print(mineblock1.get_block)
    print(mineblock1.getmine(1, 2))
    info = 0
    for i in range(BLOCK_WIDTH):
        for j in range(BLOCK_HEIGHT):
            if mineblock1.getmine(i, j):
                print(mineblock1.open_mine(i, j))
                info = 1
            if info == 1: break
        if info == 1: break
    info = 0
