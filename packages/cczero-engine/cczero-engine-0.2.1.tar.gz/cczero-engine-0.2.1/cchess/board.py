# -*- coding: utf-8 -*-
"""
Copyright (C) 2014  walker li <walker8088@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import copy

from functools import *

from .exception import *
from .piece import *
from .move import *

# -----------------------------------------------------#
FULL_INIT_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1'
EMPTY_FEN = '9/9/9/9/9/9/9/9/9/9 w - - 0 1'
UNKNOWN, RED_WIN, BLACK_WIN, PEACE = range(4)
result_str = (u"未知", u"红胜", u"黑胜", u"平局")
# -----------------------------------------------------#
_text_board = [
    # '  1   2   3   4   5   6   7   8   9 ',
    '9 ┌───┬───┬───┬───┬───┬───┬───┬───┐ ',
    '  │   │   │   │ ＼│ ／│   │   │   │ ',
    '8 ├───┼───┼───┼───┼───┼───┼───┼───┤ ',
    '  │   │　 │   │ ／│ ＼│   │   │   │ ',
    '7 ├───┼───┼───┼───┼───┼───┼───┼───┤ ',
    '  │   │　 │　 │　 │   │   │   │   │ ',
    '6 ├───┼───┼───┼───┼───┼───┼───┼───┤ ',
    '  │　 │　 │   │   │   │   │   │   │ ',
    '5 ├───┴───┴───┴───┴───┴───┴───┴───┤ ',
    '  │　                             │ ',
    '4 ├───┬───┬───┬───┬───┬───┬───┬───┤ ',
    '  │　 │　 │   │   │   │　 │　 │　 │ ',
    '3 ├───┼───┼───┼───┼───┼───┼───┼───┤ ',
    '  │   │　 │　 │　 │   │   │   │   │ ',
    '2 ├───┼───┼───┼───┼───┼───┼───┼───┤ ',
    '  │   │   │   │ ＼│ ／│　 │　 │　 │ ',
    '1 ├───┼───┼───┼───┼───┼───┼───┼───┤ ',
    '  │   │　 │   │ ／│ ＼│　 │   │   │ ',
    '0 └───┴───┴───┴───┴───┴───┴───┴───┘ ',
    '   ',
    '  a   b   c   d   e   f   g   h   i ',
    '  0   1   2   3   4   5   6   7   8 ',
    # '  九  八  七  六  五  四  三  二  一',
    # '',
]

PLAYER = ('', 'RED', 'BLACK')
PLAYER_CN = ('', '红方', '黑方')


# -----------------------------------------------------#
def _pos_to_text_board_pos(pos):
    return 4 * pos[0] + 2, (9 - pos[1]) * 2


# -----------------------------------------------------#
class ChessPlayer(object):

    def __init__(self, color):
        self.color = color

    def next(self):
        if self.color != NO_COLOR:
            self.color = 3 - self.color
        return ChessPlayer(self.color)

    def opposite(self):
        if self.color == NO_COLOR:
            return NO_COLOR
        return 3 - self.color

    def __str__(self):
        return PLAYER[self.color]

    def __eq__(self, other):
        if isinstance(other, ChessPlayer):
            return self.color == other.color
        elif isinstance(other, int):
            return self.color == other
        return False


# -----------------------------------------------------#
class BaseChessBoard(object):
    def __init__(self, fen=''):
        self.from_fen(fen)
        self.WXF = WXF(bcb=self)

    def clear(self):
        self._board = [[None for _ in range(9)] for _ in range(10)]
        self.move_player = ChessPlayer(NO_COLOR)

    def copy(self):
        return copy.deepcopy(self)

    def mirror(self):
        board = [[self._board[y][8 - x] for x in range(9)] for y in range(10)]
        self._board = board

    def flip(self):
        board = [[self._board[9 - y][x] for x in range(9)] for y in range(10)]
        self._board = board

    def swap(self):

        def swap_fench(fench):
            if fench is None: return None
            return fench.upper() if fench.islower() else fench.lower()

        self._board = [[swap_fench(self._board[y][x]) for x in range(9)] for y in range(10)]

        self.move_player.next()

    def put_fench(self, fench, pos):
        self._board[pos[1]][pos[0]] = fench

    def get_fench(self, pos):
        return self._board[pos[1]][pos[0]]

    def get_fench_color(self, pos):
        fench = self.get_fench(pos)

        if not fench:
            return None

        return RED if fench.isupper() else BLACK

    def get_fenchs(self, fench):
        poss = []
        for x in range(9):
            for y in range(10):
                if self._board[y][x] == fench:
                    poss.append((x, y))
        return poss

    def get_piece(self, pos):
        fench = self.get_fench(pos)
        return Piece.create(self, fench, pos) if fench else None

    def get_pieces(self, color=None):

        if isinstance(color, ChessPlayer):
            color = color.color

        for x in range(9):
            for y in range(10):
                fench = self._board[y][x]
                if not fench:
                    continue
                if color is None:
                    yield Piece.create(self, fench, (x, y))
                else:
                    _, p_color = fench_to_species(fench)
                    if color == p_color:
                        yield Piece.create(self, fench, (x, y))

    def get_fenchs_x(self, x, fench):
        poss = []
        for y in range(10):
            if self._board[y][x] == fench:
                poss.append((x, y))
        return poss

    def get_king(self, color):

        if isinstance(color, ChessPlayer):
            color = color.color

        limit_y = ((), (0, 1, 2), (7, 8, 9))
        for x in (3, 4, 5):
            for y in limit_y[color]:
                fench = self._board[y][x]
                if not fench:
                    continue
                if fench.lower() == 'k':
                    return Piece.create(self, fench, (x, y))
        return None

    def is_valid_move_t(self, move_t):
        return self.is_valid_move(move_t[0], move_t[1])

    def is_valid_move(self, pos_from, pos_to):
        """
        只进行最基本的走子规则检查，不对每个子的规则进行检查，以加快文件加载之类的速度
        """

        if not (0 <= pos_to[0] <= 8):
            return False
        if not (0 <= pos_to[1] <= 9):
            return False

        fench_from = self._board[pos_from[1]][pos_from[0]]
        if not fench_from:
            return False

        _, from_color = fench_to_species(fench_from)

        # move_player 不是None值才会进行走子颜色检查，这样处理某些特殊的存储格式时会处理比较迅速
        if (self.move_player != NO_COLOR) and (self.move_player != from_color):
            return False

        fench_to = self._board[pos_to[1]][pos_to[0]]
        if not fench_to:
            return True

        _, to_color = fench_to_species(fench_to)

        return from_color != to_color

    def _move_piece(self, pos_from, pos_to):

        fench = self._board[pos_from[1]][pos_from[0]]
        self._board[pos_to[1]][pos_to[0]] = fench
        self._board[pos_from[1]][pos_from[0]] = None

        return fench

    def move(self, pos_from, pos_to):

        if not self.is_valid_move(pos_from, pos_to):
            return None

        board = self.copy()
        fench = self.get_fench(pos_to)
        self._move_piece(pos_from, pos_to)

        return Move(board, pos_from, pos_to)

    def move_iccs(self, move_str):
        move_from, move_to = Move.from_iccs(move_str)
        return self.move(move_from, move_to)

    def move_chinese(self, move_str):
        move_from, move_to = Move.from_chinese(self, move_str)
        return self.move(move_from, move_to)

    def next_turn(self):
        return self.move_player.next()

    def from_fen(self, fen):

        num_set = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
        ch_set = {'k', 'a', 'b', 'n', 'r', 'c', 'p'}

        self.clear()

        if fen == '':
            return True

        fen = fen.strip()

        x = 0
        y = 9

        for i in range(0, len(fen)):
            ch = fen[i]

            if ch == ' ':
                break
            elif ch == '/':
                y -= 1
                x = 0
                if y < 0: break
            elif ch in num_set:
                x += int(ch)
                if x > 8: x = 8
            elif ch.lower() in ch_set:
                if x <= 8:
                    self.put_fench(ch, (x, y))
                    x += 1
            else:
                return False

        fens = fen.split()

        self.move_player = ChessPlayer(NO_COLOR)

        if (len(fens) >= 2) and (fens[1] == 'b'):
            self.move_player = ChessPlayer(BLACK)
        else:
            self.move_player = ChessPlayer(RED)

        return True

    def to_fen_base(self):
        fen = ''
        count = 0
        for y in range(9, -1, -1):
            for x in range(9):
                fench = self._board[y][x]
                if fench:
                    if count != 0:
                        fen += str(count)
                        count = 0
                    fen += fench
                else:
                    count += 1

            if count > 0:
                fen += str(count)
                count = 0

            if y > 0:
                fen += '/'

        fen += ' b' if self.move_player == BLACK else ' w'

        return fen

    def to_fen(self):
        return self.to_fen_base() + ' - - 0 1'

    def detect_move_pieces(self, new_board):
        p_from = []
        p_to = []
        for x in range(9):
            for y in range(10):
                p_old = self.get_fench((x, y))
                p_new = new_board.get_fench((x, y))
                # same
                if p_old == p_new:
                    continue
                # move from
                if p_new is None:
                    p_from.append((x, y))
                    # move_to
                else:
                    p_to.append((x, y))
        return p_from, p_to

    def create_move_from_board(self, new_board):
        p_froms, p_tos = self.detect_move_pieces(new_board)
        if (len(p_froms) == 1) and (len(p_tos) == 1):
            p_from = p_froms[0]
            p_to = p_tos[0]
            if self.is_valid_move(p_from, p_to):
                return p_from, p_to
        return None, None

    def text_view(self):

        board_str = _text_board[:]

        y = 0
        for line in self._board:
            x = 8
            for ch in line[::-1]:
                if ch:
                    pos = _pos_to_text_board_pos((x, y))
                    new_text = board_str[pos[1]][:pos[0]] + fench_to_txt_name(ch) + board_str[pos[1]][pos[0] + 2:]
                    board_str[pos[1]] = new_text
                x -= 1
            y += 1

        return board_str

    def print_board(self):
        print('')
        for s in self.text_view():
            print(s)

    @staticmethod
    def tuple_to_str(step):
        move_str = ''
        move_str += str(step[0][0])
        move_str += str(step[0][1])
        move_str += str(step[1][0])
        move_str += str(step[1][1])
        return move_str

    @staticmethod
    def move_to_str(x, y, x_, y_):
        move_str = ''
        move_str += str(x)
        move_str += str(y)
        move_str += str(x_)
        move_str += str(y_)
        return move_str

    @staticmethod
    def str_to_move(action: str):
        x0 = int(action[0])
        y0 = int(action[1])
        x1 = int(action[2])
        y1 = int(action[3])
        return (x0, y0), (x1, y1)

    @staticmethod
    def flip_move(x):
        new = ''
        new = ''.join([new, str(8 - int(x[0]))])
        new = ''.join([new, str(9 - int(x[1]))])
        new = ''.join([new, str(8 - int(x[2]))])
        new = ''.join([new, str(9 - int(x[3]))])
        return new

    def to_fliped_state(self):
        rows = self.to_fen().split(" ")[0].split('/')

        def swapcase(a):
            if a.isalpha():
                return a.lower() if a.isupper() else a.upper()
            return a

        def swapall(aa):
            return "".join([swapcase(a) for a in aa])

        return "/".join([swapall(reversed(row)) for row in reversed(rows)])


# -----------------------------------------------------#
class ChessBoard(BaseChessBoard):
    def __init__(self, fen=''):
        super().__init__(fen)

    @staticmethod
    def has_attack_chessman(state):
        for chessman in state:
            c = chessman.lower()
            if c == 'r' or c == 'n' or c == 'p' or c == 'c':
                return True
        return False

    def is_valid_move(self, pos_from, pos_to):
        """
        判断走子是否合理
        """
        if not super().is_valid_move(pos_from, pos_to):
            return False

        piece = self.get_piece(pos_from)
        return piece.is_valid_move(pos_to)

    def create_moves(self):
        """
        产生目前执棋方所有的走子
        """
        for piece in self.get_pieces(self.move_player):
            for move in piece.create_moves():
                yield move

    def create_piece_moves(self, pos):
        """
        产生该棋子所有的走子
        """
        piece = self.get_piece(pos)
        if piece:
            for move in piece.create_moves():
                yield move

    def is_checked_move(self, pos_from, pos_to):
        """
        该走子会被对方将军
        """
        if not self.is_valid_move(pos_from, pos_to):
            raise CChessException('Invalid Move')

        board = self.copy()
        board._move_piece(pos_from, pos_to)
        board.move_player.next()
        return board.check_count() > 0

    def is_checking_move(self, pos_from, pos_to):
        """
        该走子会将军对方
        """
        board = self.copy()
        board._move_piece(pos_from, pos_to)
        return board.check_count() > 0

    def is_checking(self):
        """
        正在将军对方
        """
        board = self.copy()
        return board.check_count() > 0

    def is_checkmate(self):
        """
        将死对方
        """
        board = self.copy()
        board.move_player.next()
        return board.is_cramp()

    def is_loss(self):
        """
        将死对方
        """
        board = self.copy()
        return board.is_cramp()

    def is_cramp(self):
        """
        无子可走的状态
        """
        for piece in self.get_pieces(self.move_player):
            for move_it in piece.create_moves():
                if self.is_valid_move_t(move_it):
                    if not self.is_checked_move(move_it[0], move_it[1]):
                        return False
        return True

    def check_count(self):
        """
        正在将军对方的棋子的计数
        """
        king = self.get_king(self.move_player.opposite())
        killers = self.get_pieces(self.move_player)
        return reduce(
            lambda count, piece: count + 1
            if piece.is_valid_move((king.x, king.y)) else count, killers, 0)

    def count_x_line_in(self, y, x_from, x_to):
        return reduce(lambda count, fench: count + 1 if fench else count,
                      self.x_line_in(y, x_from, x_to), 0)

    def count_y_line_in(self, x, y_from, y_to):
        return reduce(lambda count, fench: count + 1 if fench else count,
                      self.y_line_in(x, y_from, y_to), 0)

    def x_line_in(self, y, x_from, x_to):
        step = 1 if x_to > x_from else -1
        return [self._board[y][x] for x in range(x_from + step, x_to, step)]

    def y_line_in(self, x, y_from, y_to):
        step = 1 if y_to > y_from else -1
        return [self._board[y][x] for y in range(y_from + step, y_to, step)]


class WXF(object):
    def __init__(self, bcb=None):
        self.height = 10
        self.width = 9
        self.BaseChessBoard = bcb

    @staticmethod
    def swap_case(a):
        # if a.isalpha():
        #     return a.lower() if a.isupper() else a.upper()
        return a

    def parse_wxf(self, wxf):
        piece = self.swap_case(wxf[0])
        col = wxf[1]
        mov = wxf[2]
        dest_col = wxf[3]
        dest_row = 0
        print(piece, col, mov, dest_col)
        src_row, src_col = self.find_row(piece, col)
        if mov == '.' or mov == '=':
            dest_row = src_row
            if piece.islower():
                dest_col = int(dest_col) - 1
            else:
                dest_col = self.width - int(dest_col)
        elif mov == '+':
            if piece.islower():
                dest_col = int(dest_col) - 1
            else:
                dest_col = self.width - int(dest_col)
                dest_row = col
        # else:
        #     if piece == 'h' or piece == 'H' or piece == 'e' or piece == 'E' or piece == 'a' or piece == 'A':
        #         if piece.islower():
        #             dest_col = int(dest_col) - 1
        #         else:
        #             dest_col = self.width - int(dest_col)
        #         if piece == 'h' or piece == 'H':
        #             # for house/knight
        #             step = 1 if abs(dest_col - src_col) == 2 else 2
        #         elif piece == 'e' or piece == 'E':
        #             # for elephant/bishop
        #             step = 2
        #         else:
        #             # for advisor
        #             step = 1
        #         if mov == '+' and piece.islower() or mov == '-' and piece.isupper():
        #             dest_row = src_row + step
        #         else:
        #             dest_row = src_row - step
        #     else:
        #         # move vertically
        #         step = int(dest_col)
        #         # print(src_col, src_row, col, dest_col)
        #         if mov == '+' and piece.isupper:
        #             dest_col = 9 - step
        #             dest_row = src_row + col
        #         else:
        #             dest_row = src_row - step
        #         # dest_col = src_col
        return self.BaseChessBoard.move_to_str(src_col, src_row, dest_col, dest_row)

    def find_row(self, piece, col):
        column = 0
        row = -1
        if col.isdigit():
            if piece.isupper():
                column = self.width - int(col)
            else:
                column = int(col) - 1
            for i in range(self.height):
                if self.BaseChessBoard._board[i][int(column)] == piece:
                    row = i
                    break
        else:
            first_row = -1
            second_row = -1
            column = -1
            for j in range(self.width):
                column = -1
                for i in range(self.height):
                    if self.BaseChessBoard._board[i][j] == piece:
                        if column == -1:
                            column = j
                            first_row = i
                        else:
                            if column == j:
                                second_row = i
                                break
                            else:
                                column = j
                                first_row = second_row = -1
                if first_row != -1 and second_row != -1:
                    break
            # if (piece.islower() and col == '+') or (piece.isupper() and col == '-'):
            #     row = second_row
            # else:
            #     row = first_row
        return row, column