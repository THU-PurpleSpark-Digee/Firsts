import json
import sys
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from enum import Enum
from pygame.locals import *

import pygame

from mineblock import *
from record import Ui_MainWindow
from recordings import Records

# 游戏屏幕的宽
SCREEN_WIDTH = BLOCK_WIDTH * SIZE
# 游戏屏幕的高
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE


class GameStatus(Enum):
    readied = 1,
    started = 2,
    over = 3,
    win = 4


class ForHelp(Enum):
    Yes = 1,
    No = 0


class WinAlreadyStatus(Enum):
    Yes = 1,
    No = 0


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


class MyMainWnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("PurpleSpark.ico"))
        self.setWindowTitle("历史纪录")
        self.run()

    def run(self):
        with open("records.json", "r") as f:
            li = json.load(f)
        if len(li) >= 1:
            for idx in range(len(li)):
                self.ui.tableWidget.setItem(idx, 0, QTableWidgetItem(str(li[idx])))


def main():
    app = QApplication(sys.argv)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('扫雷')
    img = pygame.image.load("PurpleSpark.ico")
    pygame.display.set_icon(img)

    font1 = pygame.font.SysFont("Consolas", SIZE * 2)  # 得分的字体
    fwidth, fheight = font1.size('999')
    blank1 = font1.size("1234567")[0]
    blank2 = font1.size("12345")[0]
    red = (200, 40, 40)

    soundbomb = pygame.mixer.Sound("sounds/1.wav")
    soundright = pygame.mixer.Sound("sounds/2.wav")
    soundclick = pygame.mixer.Sound("sounds/3.wav")
    soundbling = pygame.mixer.Sound("sounds/bling.MP3")

    pygame.mixer.music.load("music/Summer Seaside.mp3")

    # 加载资源图片，因为资源文件大小不一，所以做了统一的缩放处理
    img0 = pygame.image.load('image/0.jpg').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('image/1.jpg').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('image/2.jpg').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('image/3.jpg').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('image/4.jpg').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('image/5.jpg').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('image/6.jpg').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('image/7.jpg').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('image/8.jpg').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_blank = pygame.image.load('image/9.jpg').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    img_flag = pygame.image.load('image/10.jpg').convert()
    img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))
    img_ask = pygame.image.load('image/questionmark.jpg').convert()
    img_ask = pygame.transform.smoothscale(img_ask, (SIZE, SIZE))
    img_mine = pygame.image.load('image/11.jpg').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    img_blood = pygame.image.load('image/12.jpg').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    img_error = pygame.image.load('image/13.jpg').convert()
    img_error = pygame.transform.smoothscale(img_error, (SIZE, SIZE))

    face_size = int(SIZE * 2)

    img_face_normal = pygame.image.load('image/14.jpg').convert()
    img_face_normal = pygame.transform.smoothscale(img_face_normal, (face_size, face_size))
    img_face_success = pygame.image.load('image/15.jpg').convert()
    img_face_success = pygame.transform.smoothscale(img_face_success, (face_size, face_size))
    img_face_fail = pygame.image.load('image/16.jpg').convert()
    img_face_fail = pygame.transform.smoothscale(img_face_fail, (face_size, face_size))
    img_time = pygame.image.load('image/17.jpg').convert()
    img_time = pygame.transform.smoothscale(img_time, (face_size, face_size))
    img_score = pygame.image.load('image/18.jpg').convert()
    img_score = pygame.transform.smoothscale(img_score, (face_size, face_size))
    img_goldcup = pygame.image.load('image/19.jpg').convert()
    img_goldcup = pygame.transform.smoothscale(img_goldcup, (face_size, face_size))
    img_help = pygame.image.load('image/20.jpg').convert()
    img_help = pygame.transform.smoothscale(img_help, (face_size, face_size))

    face_pos_x = (SCREEN_WIDTH - face_size) // 2
    face_pos_y = (SIZE * 2 - face_size) // 2
    img_help_pos_x = SCREEN_WIDTH - SIZE * 2
    img_help_pos_y = face_pos_y

    img_dict = {
        0: img0,
        1: img1,
        2: img2,
        3: img3,
        4: img4,
        5: img5,
        6: img6,
        7: img7,
        8: img8
    }

    bgcolor = (255, 190, 132)  # 背景色

    block = MineBlock()
    game_status = GameStatus.readied
    for_help_status = ForHelp.No
    start_time = None  # 开始时间
    elapsed_time = 0  # 耗时
    winalready = WinAlreadyStatus.No

    while True:
        # 填充背景色
        screen.fill(bgcolor)

        for event in pygame.event.get():

            if game_status == GameStatus.over or game_status == GameStatus.win:
                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if face_pos_x <= mouse_x <= face_pos_x + face_size \
                            and face_pos_y <= mouse_y <= face_pos_y + face_size:
                        game_status = GameStatus.readied
                        block = MineBlock()
                        start_time = time.time()
                        winalready = WinAlreadyStatus.No
                        elapsed_time = 0
                    elif 0 <= mouse_x <= face_size and face_pos_y <= mouse_y <= face_pos_y + face_size:
                        wnd = MyMainWnd()
                        wnd.show()
                    else:
                        sys.exit()

            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2
                b1, b2, b3 = pygame.mouse.get_pressed()
                if y >= 0:
                    if game_status == GameStatus.started:
                        # 鼠标左右键同时按下，如果已经标记了所有雷，则打开周围一圈
                        # 如果还未标记完所有雷，则有一个周围一圈被同时按下的效果
                        if b1 and b3:
                            mine = block.getmine(x, y)
                            if mine.status == BlockStatus.opened:
                                if not block.double_mouse_button_down(x, y):
                                    game_status = GameStatus.over
                                    soundbomb.play(0)
                                    pygame.mixer.music.stop()
                                    pygame.mixer.music.load("music/The truth that you leave.mp3")
                                    pygame.mixer.music.play(-1, 0)

            elif event.type == MOUSEBUTTONUP:
                if y < 0:
                    if face_pos_x <= mouse_x <= face_pos_x + face_size \
                            and face_pos_y <= mouse_y <= face_pos_y + face_size:
                        game_status = GameStatus.readied
                        pygame.mixer.music.stop()
                        block = MineBlock()
                        start_time = time.time()
                        winalready = WinAlreadyStatus.No
                        elapsed_time = 0
                        continue
                    # 按下表情，重置游戏
                    elif img_help_pos_x <= mouse_x <= img_help_pos_x + face_size \
                            and img_help_pos_y <= mouse_y <= img_help_pos_y + face_size:
                        for_help_status = ForHelp.Yes
                        soundbling.play(0)
                    elif 0 <= mouse_x <= face_size and face_pos_y <= mouse_y <= face_pos_y + face_size:
                        wnd = MyMainWnd()
                        wnd.show()

                else:
                    if game_status == GameStatus.readied:

                        mine = block.getmine(x, y)
                        if b1 and not b3:  # 按鼠标左键
                            if not block.open_mine(x, y):
                                while True:
                                    block = MineBlock()
                                    if block.open_mine(x, y):
                                        break
                            soundclick.play(0)

                        game_status = GameStatus.started
                        pygame.mixer.music.load("music/Summer Seaside.mp3")
                        pygame.mixer.music.play(-1, 0)
                        start_time = time.time()
                        elapsed_time = 0

                    if game_status == GameStatus.started:
                        mine = block.getmine(x, y)
                        if b1 and not b3:  # 按鼠标左键
                            if mine.status == BlockStatus.normal or mine.status == BlockStatus.ask:
                                if not block.open_mine(x, y):
                                    if for_help_status == ForHelp.No:
                                        game_status = GameStatus.over
                                        pygame.mixer.music.stop()
                                        pygame.mixer.music.load("music/The truth that you leave.mp3")
                                        pygame.mixer.music.play(-1, 0)
                                        soundbomb.play(0)
                                    else:
                                        mine.status = BlockStatus.flag
                                        soundclick.play(0)
                                else:
                                    soundclick.play(0)
                                for_help_status = ForHelp.No
                        elif not b1 and b3:  # 按鼠标右键
                            if mine.status == BlockStatus.normal:
                                mine.status = BlockStatus.flag
                                soundclick.play(0)
                            elif mine.status == BlockStatus.flag:
                                mine.status = BlockStatus.ask
                                soundclick.play(0)
                            elif mine.status == BlockStatus.ask:
                                mine.status = BlockStatus.normal
                                soundclick.play(0)
                        elif b1 and b3:
                            if mine.status == BlockStatus.double:
                                block.double_mouse_button_up(x, y)

                                soundright.play(0)

        flag_count = 0
        opened_count = 0

        for row in block.block:
            for mine in row:
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if mine.status == BlockStatus.opened:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                    opened_count += 1
                elif mine.status == BlockStatus.double:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                elif mine.status == BlockStatus.bomb:
                    screen.blit(img_blood, pos)
                elif not mine.value and mine.status == BlockStatus.flag and game_status == GameStatus.over:
                    screen.blit(img_error, pos)
                elif mine.value and game_status == GameStatus.win:
                    screen.blit(img_flag, pos)
                elif mine.status == BlockStatus.flag:
                    screen.blit(img_flag, pos)
                    flag_count += 1
                elif game_status == GameStatus.over and mine.value:
                    screen.blit(img_mine, pos)
                elif mine.status == BlockStatus.ask:
                    screen.blit(img_ask, pos)
                elif mine.status == BlockStatus.hint:
                    screen.blit(img0, pos)

                elif mine.status == BlockStatus.normal:
                    screen.blit(img_blank, pos)

        print_text(screen, font1, blank1 - 0.25 * SIZE, (SIZE * 2 - fheight) // 2 + 0.15 * SIZE,
                   '%02d' % (MINE_COUNT - flag_count), red)
        if game_status == GameStatus.started:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, font1, SCREEN_WIDTH - fwidth - blank2 + 0.25 * SIZE, (SIZE * 2 - fheight) // 2 + 0.15 * SIZE,
                   '%03d' % elapsed_time, red)

        if opened_count == BLOCK_WIDTH * BLOCK_HEIGHT - MINE_COUNT:
            game_status = GameStatus.win
            if winalready == WinAlreadyStatus.No:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/Octopath Traveler.mp3")
                pygame.mixer.music.play(-1, 0)
                winalready = WinAlreadyStatus.Yes

                Records(elapsed_time)

        screen.blit(img_score, (SIZE * 5, face_pos_y))
        screen.blit(img_goldcup, (0, face_pos_y))
        screen.blit(img_time, (SCREEN_WIDTH - SIZE * 11, face_pos_y))
        screen.blit(img_help, (img_help_pos_x, img_help_pos_y))
        if game_status == GameStatus.over:
            screen.blit(img_face_fail, (face_pos_x, face_pos_y))
        elif game_status == GameStatus.win:
            screen.blit(img_face_success, (face_pos_x, face_pos_y))
        else:
            screen.blit(img_face_normal, (face_pos_x, face_pos_y))

        pygame.display.update()


if __name__ == '__main__':
    main()
