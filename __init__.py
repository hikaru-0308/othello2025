# Generation ID: Hutch_1765415473877_7ifzxg1wu (前半)

from collections import deque
from copy import deepcopy

def myai(board, color):
    """
    オセロAI: 序盤～終盤に応じた戦略で最適な手を返す
    """

    evaluation_table = [
        [10, 5, 5, 5, 5, 10],
        [5, 1, 2, 2, 1, 5],
        [5, 2, 0, 0, 2, 5],
        [5, 2, 0, 0, 2, 5],
        [5, 1, 2, 2, 1, 5],
        [10, 5, 5, 5, 5, 10]
    ]

    opponent_color = 3 - color
    move_count = count_stones(board)

    if move_count <= 8:
        depth = 3
        use_min_stones = True
    elif move_count <= 20:
        depth = 5
        use_min_stones = False
    else:
        depth = 5
        use_min_stones = False

    valid_moves = get_valid_moves(board, color)

    if not valid_moves:
        return None

    best_move = None
    best_score = float('-inf')

    for move in valid_moves:
        score = bfs_evaluate(board, color, move, depth, evaluation_table, use_min_stones)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def count_stones(board):
    """盤面の総石数を計算"""
    count = 0
    for row in board:
        for cell in row:
            if cell != 0:
                count += 1
    return count


def get_valid_moves(board, color):
    """指定された色の有効な手をすべて取得"""
    valid_moves = []
    for row in range(6):
        for col in range(6):
            if board[row][col] == 0 and is_valid_move(board, row, col, color):
                valid_moves.append((col, row))
    return valid_moves


def is_valid_move(board, row, col, color):
    """指定位置が有効な手かチェック"""
    if board[row][col] != 0:
        return False

    opponent = 3 - color
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        if has_flippable(board, row, col, dr, dc, color, opponent):
            return True

    return False


def has_flippable(board, row, col, dr, dc, color, opponent):
    """指定方向に反転できる石があるかチェック"""
    r, c = row + dr, col + dc
    found_opponent = False

    while 0 <= r < 6 and 0 <= c < 6:
        if board[r][c] == 0:
            return False
        if board[r][c] == opponent:
            found_opponent = True
        elif board[r][c] == color:
            return found_opponent
        r += dr
        c += dc

    return False


def place_stone(board, row, col, color):
    """石を配置し、反転可能な石をすべて反転"""
    board[row][col] = color
    opponent = 3 - color
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        flip_stones(board, row, col, dr, dc, color, opponent)


def flip_stones(board, row, col, dr, dc, color, opponent):
    """指定方向の石を反転"""
    positions = []
    r, c = row + dr, col + dc

    while 0 <= r < 6 and 0 <= c < 6 and board[r][c] == opponent:
        positions.append((r, c))
        r += dr
        c += dc

    if 0 <= r < 6 and 0 <= c < 6 and board[r][c] == color:
        for pr, pc in positions:
            board[pr][pc] = color


def bfs_evaluate(board, color, move, depth, eval_table, use_min_stones):
    """幅優先探索で手を評価"""
    queue = deque()
    board_copy = deepcopy(board)
    place_stone(board_copy, move[1], move[0], color)

    queue.append((board_copy, color, 1))

    scores = []

    while queue:
        current_board, current_color, current_depth = queue.popleft()

        if current_depth == depth:
            scores.append(evaluate_board(current_board, eval_table))
            continue

        next_color = 3 - current_color
        next_moves = get_valid_moves(current_board, next_color)

        if not next_moves:
            next_moves_alt = get_valid_moves(current_board, current_color)
            if next_moves_alt:
                next_color = current_color
                next_moves = next_moves_alt
            else:
                scores.append(evaluate_board(current_board, eval_table))
                continue

        for next_move in next_moves:
            new_board = deepcopy(current_board)
            place_stone(new_board, next_move[1], next_move[0], next_color)
            queue.append((new_board, next_color, current_depth + 1))

    if not scores:
        return evaluate_board(board_copy, eval_table)

    if use_min_stones:
        return min(scores)
    else:
        return max(scores)


def evaluate_board(board, eval_table):
    """評価表に基づいて盤面を評価"""
    score = 0
    for row in range(6):
        for col in range(6):
            if board[row][col] != 0:
                score += eval_table[row][col]
    return score

# Generation ID: Hutch_1765415473877_7ifzxg1wu (後半)
