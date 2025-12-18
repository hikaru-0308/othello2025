# Othello AI : 指定仕様準拠
# 6x6 / 8x8 対応
# BLACK = 1, WHITE = 2, EMPTY = 0

import copy

EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = [
    (-1,-1),(-1,0),(-1,1),
    (0,-1),        (0,1),
    (1,-1),(1,0),(1,1)
]

# ---------------- 基本 ----------------
def size(board):
    return len(board)


def inside(x, y, n):
    return 0 <= x < n and 0 <= y < n


def opponent(color):
    return BLACK if color == WHITE else WHITE

# ---------------- 合法手 ----------------
def is_valid(board, x, y, color):
    n = size(board)
    if not inside(x, y, n) or board[x][y] != EMPTY:
        return False
    opp = opponent(color)
    for dx, dy in DIRECTIONS:
        nx, ny = x+dx, y+dy
        found = False
        while inside(nx, ny, n) and board[nx][ny] == opp:
            found = True
            nx += dx
            ny += dy
        if found and inside(nx, ny, n) and board[nx][ny] == color:
            return True
    return False


def legal_moves(board, color):
    n = size(board)
    return [(x,y) for x in range(n) for y in range(n)
            if is_valid(board, x, y, color)]

# ---------------- 着手 ----------------
def put(board, x, y, color):
    n = size(board)
    b = copy.deepcopy(board)
    b[x][y] = color
    opp = opponent(color)
    for dx, dy in DIRECTIONS:
        nx, ny = x+dx, y+dy
        path = []
        while inside(nx, ny, n) and b[nx][ny] == opp:
            path.append((nx, ny))
            nx += dx
            ny += dy
        if path and inside(nx, ny, n) and b[nx][ny] == color:
            for px, py in path:
                b[px][py] = color
    return b

# ---------------- 評価 ----------------
WEIGHT_6 = [
    [100,-20,10,10,-20,100],
    [-20,-50,-2,-2,-50,-20],
    [10,-2,-1,-1,-2,10],
    [10,-2,-1,-1,-2,10],
    [-20,-50,-2,-2,-50,-20],
    [100,-20,10,10,-20,100]
]

WEIGHT_8 = [
    [100,-20,10, 5, 5,10,-20,100],
    [-20,-50,-2,-2,-2,-2,-50,-20],
    [10,-2,-1,-1,-1,-1,-2,10],
    [5,-2,-1,-1,-1,-1,-2,5],
    [5,-2,-1,-1,-1,-1,-2,5],
    [10,-2,-1,-1,-1,-1,-2,10],
    [-20,-50,-2,-2,-2,-2,-50,-20],
    [100,-20,10,5,5,10,-20,100]
]


def evaluate(board, color):
    n = size(board)
    W = WEIGHT_6 if n == 6 else WEIGHT_8
    opp = opponent(color)
    score = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == color:
                score += W[i][j]
            elif board[i][j] == opp:
                score -= W[i][j]
    # mobility
    score += 2 * (len(legal_moves(board, color))
                  - len(legal_moves(board, opp)))
    return score

# ---------------- 終盤完全読み ----------------
def disc_diff(board, color):
    opp = opponent(color)
    s = 0
    for row in board:
        for c in row:
            if c == color: s += 1
            elif c == opp: s -= 1
    return s


def exact(board, color):
    moves = legal_moves(board, color)
    opp = opponent(color)
    if not moves:
        if not legal_moves(board, opp):
            return disc_diff(board, color)
        return -exact(board, opp)
    best = -10**9
    for x,y in moves:
        v = -exact(put(board,x,y,color), opp)
        best = max(best, v)
    return best

# ---------------- αβ探索 ----------------
def alphabeta(board, depth, a, b, color):
    moves = legal_moves(board, color)
    opp = opponent(color)
    if depth == 0 or not moves:
        return evaluate(board, color), None
    best_move = None
    for x,y in moves:
        v,_ = alphabeta(put(board,x,y,color), depth-1, -b, -a, opp)
        v = -v
        if v > a:
            a = v
            best_move = (x,y)
        if a >= b:
            break
    return a, best_move

# ---------------- AI本体 ----------------
def myai(board, color):
    moves = legal_moves(board, color)
    if not moves:
        return None

    empty = sum(r.count(EMPTY) for r in board)
    opp = opponent(color)

    # 残り8手：完全読み
    if empty <= 8:
        best = -10**9
        best_move = None
        for x,y in moves:
            v = -exact(put(board,x,y,color), opp)
            if v > best:
                best = v
                best_move = (y, x)  # column, row
        return best_move

    # 残り18手：深さ6
    depth = 6 if empty <= 18 else 4
    _, move = alphabeta(board, depth, -10**9, 10**9, color)

    # 出力は {column, row}
    return (move[1], move[0])
