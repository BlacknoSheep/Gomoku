SCORE = [[10, 100, 1000, 10000, 100000],
         [1, 10, 100, 1000, 100000]]


def calc_line_score(line):
    """
    计算一条直线上的分数
    :param line: 列表，-1黑子，0空位，1白子
    :return: 分数，黑子得分负，白子正
    """
    line_length = len(line)
    if line_length < 5:  # 不可能连成5子
        return 0
    left_blank = 0
    right_blank = 0
    score = 0  # 得分
    i = 0
    while i < line_length:  # 从前往后搜索
        score_x = 0  # 活棋索引0，半活棋索引1
        length = 0  # 连子长度
        if line[i] == 0:  # 全局左侧空位，若line内无棋子则只会运行这一句，score不改变（=0）
            left_blank += 1
            i += 1
            continue
        else:  # 黑子or白子
            color = line[i]
            length += 1
            while i + 1 < line_length and line[i + 1] == color:  # 连子数
                length += 1
                i += 1  # 表示该点已扫描
            while i + 1 < line_length and line[i + 1] == 0:  # 右侧空位数
                right_blank += 1
                i += 1  # 表示该点已扫描
        if left_blank + length + right_blank >= 5:  # 只有在可能连成5子时才计算得分
            if length > 5:
                length = 5
            if left_blank == 0 or right_blank == 0:  # 半活棋
                score_x = 1
            score_y = length - 1  # 列索引
            if color == -1:
                score -= SCORE[score_x][score_y] * 1  # 增大负值惩罚
            else:
                score += SCORE[score_x][score_y]
        left_blank = right_blank  # 本连子的右侧空位为下一个连子的左侧空位
        right_blank = 0  # 右侧空白从0开始重新计数
        i += 1
    return score


def calc_score(board, old_score):
    """
    计算盘面分数（只计算，不更新任何状态）
    :param board: 盘面（落子后）
    :param old_score: 分数（落子前）
    :return: 分数（落子后）
    """
    board_copy = board.copy()
    x, y, color = board_copy.pop()  # 当前落子
    score = old_score  # 盘面分数

    # 四个方向四条线：
    len_LT2RB = 15 - abs(x - y)  # \
    len_RT2LB = (x + y + 1) if x + y <= 14 else (28 - x - y + 1)  # /
    lines = [[0] * 15,  # －
             [0] * 15,  # |
             [0] * len_LT2RB,  # \
             [0] * len_RT2LB]  # /

    for point in board_copy:
        px, py, pc = point
        if py == y:  # 同行-
            lines[0][px] = pc
        elif px == x:  # 同列|
            lines[1][py] = pc
        elif px - x == py - y:  # \
            if x < y:
                lines[2][px] = pc
            else:
                lines[2][py] = pc
        elif px - x == -(py - y):  # /
            if x + y < 14:
                lines[3][py] = pc  # 用py保证是从右上到左下
            else:
                lines[3][14 - px] = pc

    # -旧分数+新分数
    # -
    score -= calc_line_score(lines[0])  # -落子前
    lines[0][x] = color  # 落子后
    score += calc_line_score(lines[0])  # +落子后
    # |
    score -= calc_line_score(lines[1])
    lines[1][y] = color
    score += calc_line_score(lines[1])
    # \
    score -= calc_line_score(lines[2])
    if x < y:
        lines[2][x] = color
    else:
        lines[2][y] = color
    score += calc_line_score(lines[2])
    # /
    score -= calc_line_score(lines[3])
    if x + y < 14:
        lines[3][y] = color  # 用y保证是从右上到左下
    else:
        lines[3][14 - x] = color
    score += calc_line_score(lines[3])

    # 算分出了点问题，测试一下
    # scores_print = []
    # for i in range(4):
    #     scores_print.append(calc_line_score(lines[i]))
    # print(scores_print)
    # print(lines[1])

    return score


def calc_from_beginning(board):
    """从头开始计算整个盘面的分数"""
    return 0






