import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP
import sys

from score import calc_score
from algorithms import max_value, maxmin, alpha_beta_max

# 扫描方向：-|\/
DX = [1, 0, 1, -1]
DY = [0, 1, 1, 1]


class WuZiQi:
    def __init__(self):
        pygame.init()

        # 棋盘参数
        self.MARGIN = 40  # 边距20
        self.SQUARE = 40  # 小格子边长40
        self.screen_size = self.MARGIN * 2 + self.SQUARE * 14  # 窗口尺寸
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        self.screen_color = [205, 133, 63]  # 窗口：棕色
        self.line_color = [0, 0, 0]  # 棋盘线：黑色
        self.rect_color = [0, 255, 0]  # 提示框：绿色

        # 下棋参数
        self.mode = "human"  # 模式，human人人，machine人机
        self.power = 0  # 人机难度，默认maxmin算法
        self.game_replay = True
        self.last_rect = (7, 7)  # 提示框位置
        # 默认先手用黑子
        self.current_color = -1  # -1黑子，1白子
        self.board_state = []  # 当前落子情况，(x, y, color)组成的list，0黑子，1白子
        self.current_score = 0

    def color2RGB(self, color):
        """依据color来得到对应的棋子颜色"""
        if color == -1:  # -1黑子
            return [0, 0, 0]
        else:  # 1白子
            return [255, 255, 255]

    def xy2real(self, x, y):
        """计算真实坐标"""
        real_x = self.MARGIN + self.SQUARE * x
        real_y = self.MARGIN + self.SQUARE * y
        return real_x, real_y

    def real2xy(self, real_x, real_y):
        """计算棋盘坐标"""
        x = round((real_x - self.MARGIN) / self.SQUARE)
        y = round((real_y - self.MARGIN) / self.SQUARE)
        return x, y

    def in_border(self, real_x, real_y):
        """判断该真实坐标是否在棋盘内"""
        if real_x < self.MARGIN - self.SQUARE / 2 or real_x > self.screen_size - self.SQUARE / 2 \
                or real_y < self.MARGIN - self.SQUARE / 2 or real_y > self.screen_size - self.SQUARE / 2:
            return False
        return True

    def put_point(self, x, y, color):
        """落子"""
        self.board_state.append((x, y, color))
        self.update_score()  # 更新盘面分数
        self.draw_board()  # 更新盘面
        pygame.display.update()  # 刷新窗口

        print(self.current_score)

    def check_win(self):
        """检查是否获胜"""
        x, y, color = self.board_state[-1]  # 要检查的棋子
        # line = 0  # 连子长度
        # i = x
        # j = y

        # 对当前点重复数了一次，所以五子相连时line=6
        for direction in range(4):  # 扫描方向：-|\/
            line = 0  # 连子长度
            for p in [-1, 1]:  # 前后都要检查
                i = x  # 重置到当前位置
                j = y
                while 0 <= i <= 14 and 0 <= j <= 14:  # 没有超过边界
                    if (i, j, color) in self.board_state:  # 若为同色
                        line += 1  # 连子长度+1
                        # 检查下一个位置
                        i += p * DX[direction]
                        j += p * DY[direction]
                    else:  # 否则遇到异色子或空位
                        break
            if line > 5:  # 注意由于重复计数一次，五子相连时line=6
                return True
        return False

    def change_mode(self, mode="human", power=0):
        self.mode = mode
        self.power = power

    def change_player(self):
        """轮到下一名玩家"""
        if self.mode == "machine":  # 若为人机模式
            self.current_color = -self.current_color
            if self.power == -1:
                pos, _ = max_value(self.board_state, self.current_score)
            elif self.power == 1:
                pos, _ = alpha_beta_max(self.board_state, self.current_score, depth=2)
            else:  # 默认maxmin算法
                pos, _ = maxmin(self.board_state, self.current_score, depth=1)
            x, y = pos
            self.put_point(x, y, self.current_color)
            # 检查是否获胜
            if self.check_win():
                self.end_game()
        self.current_color = -self.current_color

    # def undo1(self):
    #     """悔棋1步，用于人人"""
    #     global self.current_color
    #     if self.board_state:  # 若不为空
    #         self.board_state.remove(-1)
    #         player_id = not self.current_color
    #         return True
    #     return False  # 已经无法继续悔棋
    #
    #
    # def undo2(self):
    #     """悔棋2步，用于人机"""
    #     if self.board_state:  # 若不为空
    #         self.board_state.remove(-1)
    #         self.board_state.remove(-1)
    #         return True
    #     return False  # 已经无法继续悔棋

    def update_score(self):
        """更新棋盘分数"""
        self.current_score = calc_score(self.board_state, self.current_score)
        return 0

    def draw_board(self):
        """绘制当前盘面"""
        self.screen.fill(self.screen_color)  # 填充屏幕

        # 画外框线
        pygame.draw.line(self.screen, self.line_color, self.xy2real(0, 0), self.xy2real(14, 0), 2)
        pygame.draw.line(self.screen, self.line_color, self.xy2real(0, 14), self.xy2real(14, 14), 2)
        pygame.draw.line(self.screen, self.line_color, self.xy2real(0, 0), self.xy2real(0, 14), 2)
        pygame.draw.line(self.screen, self.line_color, self.xy2real(14, 0), self.xy2real(14, 14), 2)
        # 画内框线
        for i in range(1, 14):
            pygame.draw.line(self.screen, self.line_color, self.xy2real(0, i), self.xy2real(14, i))  # 画横线
            pygame.draw.line(self.screen, self.line_color, self.xy2real(i, 0), self.xy2real(i, 14))  # 画竖线

        # 画小黑点
        for i in [3, 7, 11]:
            for j in [3, 7, 11]:
                pygame.draw.circle(self.screen, self.line_color, self.xy2real(i, j), 5)

        # 画当前落子情况
        for point in self.board_state:
            x, y, color = point
            pygame.draw.circle(self.screen, self.color2RGB(color), self.xy2real(x, y), 20)

        # 画提示框
        x, y = self.last_rect
        real_x, real_y = self.xy2real(x, y)
        pygame.draw.rect(self.screen, self.rect_color,
                         [real_x - self.SQUARE / 2, real_y - self.SQUARE / 2, self.SQUARE, self.SQUARE], 1)

    # 结束游戏
    def end_game(self):
        self.draw_board()
        text_color = [255, 0, 0]  # 文本：红色
        text = pygame.font.SysFont("宋体", 50)  # 文本字体
        winner = "WHITE" if self.current_color == 1 else "BLACK"
        text_end = text.render(winner + " WIN!", True, text_color)
        self.screen.blit(text_end, (self.screen_size / 2 - 100, self.screen_size / 2 - 15))  # 渲染文本

        text_replay = text.render("REPLAY", True, text_color)
        rect_replay = [self.screen_size / 2 - 70, self.screen_size / 2 + 30, 140, 30]
        self.screen.blit(text_replay, (rect_replay[0], rect_replay[1]))  # 渲染文本
        pygame.draw.rect(self.screen, self.rect_color, rect_replay, 1)

        pygame.display.update()  # 刷新窗口

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:  # 退出
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP and event.button == 1:  # 鼠标左键按下
                    mouse_x, mouse_y = event.pos
                    # 若选中REPLAY
                    if rect_replay[0] < mouse_x < rect_replay[0] + rect_replay[2] and \
                            rect_replay[1] < mouse_y < rect_replay[1] + rect_replay[3]:
                        self.game_replay = True
                        return False

    def new_game(self):
        """重新开始游戏初始化参数"""
        self.game_replay = False
        self.last_rect = (7, 7)  # 提示框位置
        self.current_color = -1  # -1黑子，1白子
        self.board_state[:] = []  # 当前落子情况，(x, y, color)组成的list，0黑子，1白子
        self.current_score = 0

    def run_game(self):
        while True:
            if self.game_replay:  # 重新开始游戏，清空上局的数据
                self.new_game()
                self.draw_board()  # 刷新窗口

            # 检测鼠标
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.in_border(mouse_x, mouse_y):
                x, y = self.real2xy(mouse_x, mouse_y)  # 鼠标坐标映射到最近的棋盘坐标
                if (x, y) != self.last_rect:  # 只在提示框发生位置变化时重绘
                    self.last_rect = (x, y)
                    self.draw_board()  # 更新盘面
                    pygame.display.update()  # 刷新窗口

            # 检测键盘和鼠标事件
            for event in pygame.event.get():
                if event.type == QUIT:  # 退出
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP and event.button == 1:  # 鼠标左键按下
                    mouse_x, mouse_y = event.pos
                    if self.in_border(mouse_x, mouse_y):  # 若落子位置未出界
                        x, y = self.real2xy(mouse_x, mouse_y)
                        if (x, y, -1) not in self.board_state and (x, y, 1) not in self.board_state:  # 且该位置为空
                            self.put_point(x, y, self.current_color)  # 落子

                            # 检查是否获胜
                            if self.check_win():
                                self.end_game()
                                continue

                            self.change_player()  # 轮到对方
