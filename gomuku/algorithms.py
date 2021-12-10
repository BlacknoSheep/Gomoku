"""
为了加速，maxmin（minmax）最后一层是max_value（min_value）
所以maxmin实际深度=depth+1
alpha_beta_max深度=depth，深度为0时函数不成立
"""
import numpy as np
from score import calc_score


def available_positions(board):
    """统计可落子的位置"""
    # 此处扫描已落子的位置，但也可以实时更新+
    # 认为周围3x3范围内要有子
    # 有子：1，可落子位置：2，其他空位：0
    board_xy = np.zeros((15, 15))  # 棋盘矩阵，只考虑是否有子
    for point in board:
        x, y, color = point
        board_xy[x][y] = 1
        # 扫描周围8个位置
        i = x - 1
        while i <= x + 1:
            if 0 <= i <= 14:  # 横坐标未出界
                j = y - 1
                while j <= y + 1:
                    if 0 <= j <= 14:  # 纵坐标未出界
                        if board_xy[i][j] == 0:
                            board_xy[i][j] = 2
                    j += 1
            i += 1
    positions = []
    for i in range(15):
        for j in range(15):
            if board_xy[i][j] == 2:
                positions.append((i, j))
    return positions


def max_value(board, current_score):
    """
    max_value算法求下一个落子位置(最简单的算法)
    :param board: 当前棋盘状态
    :param current_score: 当前棋盘分数
    :return: 下一个落子坐标和对应分数
    """
    color = -board[-1][2]  # 颜色与最后一个落子相反
    positions = available_positions(board)
    board_copy = board.copy()
    max_val = float("-inf")  # 负无穷
    max_position = positions[0]
    for pos in positions:
        board_copy.append((pos[0], pos[1], color))  # 尝试落子在pos
        score = calc_score(board_copy, current_score)
        if max_val < score:
            max_val = score
            max_position = pos
        board_copy.pop()  # 取消这次尝试
    return max_position, max_val


def min_value(board, current_score):
    """
    min_value算法求下一个落子位置
    :param board: 当前棋盘状态
    :param current_score: 当前棋盘分数
    :return: 下一个落子坐标和对应分数
    """
    color = -board[-1][2]  # 颜色与最后一个落子相反
    positions = available_positions(board)
    board_copy = board.copy()
    min_val = float("inf")  # 正无穷
    min_position = positions[0]
    for pos in positions:
        board_copy.append((pos[0], pos[1], color))  # 尝试落子在pos
        score = calc_score(board_copy, current_score)
        if min_val > score:
            min_val = score
            min_position = pos
        board_copy.pop()  # 取消这次尝试
    return min_position, min_val


def maxmin(board, current_score, depth=0):
    """取下一层的最大值"""
    color = -board[-1][2]  # 颜色与最后一个落子相反
    positions = available_positions(board)
    board_copy = board.copy()
    max_val = float("-inf")  # 负无穷
    max_position = positions[0]
    if depth == 0:  # 深度为0，终止递归
        return max_value(board, current_score)  # 这里没有继续递归下去，速度更快
    for pos in positions:
        board_copy.append((pos[0], pos[1], color))  # 尝试落子在pos
        if win_state(board_copy):  # 已经获胜的没必要继续搜索分支
            return pos, float("inf")
        _, score = minmax(board_copy, calc_score(board_copy, current_score), depth - 1)
        if max_val < score:
            max_val = score
            max_position = pos
        board_copy.pop()  # 取消这次尝试
    return max_position, max_val


def minmax(board, current_score, depth=0):
    """取下一层的最小值"""
    color = -board[-1][2]  # 颜色与最后一个落子相反
    positions = available_positions(board)
    board_copy = board.copy()
    min_val = float("inf")  # 正无穷
    min_position = positions[0]
    if depth == 0:  # 深度为0，终止递归
        return min_value(board, current_score)  # 这里没有继续递归下去，速度更快
    for pos in positions:
        board_copy.append((pos[0], pos[1], color))  # 尝试落子在pos
        if win_state(board_copy):  # 已经获胜的没必要继续搜索分支
            return pos, float("-inf")
        _, score = maxmin(board_copy, calc_score(board_copy, current_score), depth - 1)
        if min_val > score:
            min_val = score
            min_position = pos
        board_copy.pop()  # 取消这次尝试
    return min_position, min_val


def alpha_beta_max(board, current_score, depth=1, alpha=float('-inf'), beta=float('inf')):
    """
    alpha-beta剪枝算法
    取下一层的最大值
    """
    color = -board[-1][2]  # 颜色与最后一个落子相反
    positions = available_positions(board)
    board_copy = board.copy()
    max_position = positions[0]
    if depth == 0:  # 深度为0，终止递归，什么也没干，所以depth至少要设为1
        return board[-1], current_score
    for pos in positions:
        board_copy.append((pos[0], pos[1], color))  # 尝试落子在pos
        if win_state(board_copy):  # 已经获胜的没必要继续搜索分支
            return pos, float("inf")
        p, score = alpha_beta_min(board_copy, calc_score(board_copy, current_score), depth - 1, alpha, beta)
        if score > alpha:
            alpha = score
            max_position = pos
        if alpha >= beta:
            board_copy.pop()  # 取消这次尝试
            return p, beta
        board_copy.pop()  # 取消这次尝试
    return max_position, alpha


def alpha_beta_min(board, current_score, depth=1, alpha=float('-inf'), beta=float('inf')):
    """
    alpha-beta剪枝算法
    取下一层的最小值
    """
    color = -board[-1][2]  # 颜色与最后一个落子相反
    positions = available_positions(board)
    board_copy = board.copy()
    min_position = positions[0]
    if depth == 0:  # 深度为0，终止递归
        return board[-1], current_score
    for pos in positions:
        board_copy.append((pos[0], pos[1], color))  # 尝试落子在pos
        if win_state(board_copy):  # 已经获胜的没必要继续搜索分支
            return pos, float("-inf")
        p, score = alpha_beta_max(board_copy, calc_score(board_copy, current_score), depth - 1, alpha, beta)
        if beta > score:
            beta = score
            min_position = pos
        if alpha >= beta:
            board_copy.pop()  # 取消这次尝试
            return p, alpha
        board_copy.pop()  # 取消这次尝试
    return min_position, beta


# 扫描方向：-|\/
DX = [1, 0, 1, -1]
DY = [0, 1, 1, 1]


def win_state(board):
    """五连的情况必定胜利，无需继续分支"""
    # 自己活四，对方无5的情况也必胜，但一一检查太麻烦了
    # 和check_win函数很像
    x, y, color = board[-1]  # 要检查的棋子

    # 对当前点重复数了一次，所以五子相连时line=6
    for direction in range(4):  # 扫描方向：-|\/
        line = 0  # 连子长度
        free = 0  # 是否为活棋
        for p in [-1, 1]:  # 前后都要检查
            i = x  # 重置到当前位置
            j = y
            while 0 <= i <= 14 and 0 <= j <= 14:  # 没有超过边界
                if (i, j, color) in board:  # 若为同色
                    line += 1  # 连子长度+1
                    # 检查下一个位置
                    i += p * DX[direction]
                    j += p * DY[direction]
                elif (i, j, -color) in board:  # 遇到异色子
                    break
                else:  # 空位
                    free += 1
                    break
        if line > 5:  # 注意由于重复计数一次，五子相连时line=6
            return True
        # elif line == 5 and free == 2:  # 活四
        #     return True
    return False
