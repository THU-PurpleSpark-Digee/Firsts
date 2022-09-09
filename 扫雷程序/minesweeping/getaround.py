BLOCK_WIDTH = 30
BLOCK_HEIGHT = 16


def _get_around(x, y):
    """返回(x, y)周围的点的坐标"""
    # 这里注意，range 末尾是开区间，所以要加 1
    return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1)
            for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) if i != x or j != y]


if __name__ == '__main__':
    print(_get_around(13, 3))
    print(_get_around(0, 3))
    print(_get_around(0, 0))
