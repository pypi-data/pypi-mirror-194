#! /usr/bin/env python
# -*- coding: utf-8 -*-

# pycchess - just another chinese chess UI
# Copyright (C) 2011 - 2015 timebug

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# import pygame

RED, BLACK = 1, 0
BORDER, SPACE = 15, 56
LOCAL, OTHER = 0, 1
NETWORK, AI = 0, 1
KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN, NONE = 0, 1, 2, 3, 4, 5, 6, -1

AI_SEARCH_DEPTH = 5

init_fen = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR r - - 0 1'
# init_fen = 'rkemsmekr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RKEMSMEKR r - - 0 1'


fen_to_str = {
    '黑车': 'r',
    '黑马': 'n',
    '黑象': 'b',
    '黑士': 'a',
    '黑将': 'k',
    '黑炮': 'c',
    '黑卒': 'p',
    '红车': 'R',
    '红马': 'N',
    '红相': 'B',
    '红仕': 'A',
    '红帅': 'K',
    '红炮': 'C',
    '红兵': 'P',
}

str_to_fen = {
    'b_che': '黑车',
    'b_ma': '黑马',
    'b_xiang': '黑象',
    'b_shi': '黑士',
    'b_jiang': '黑将',
    'b_pao': '黑炮',
    'b_bing': '黑卒',
    'r_bing': '红兵',
    'r_pao': '红炮',
    'r_che': '红车',
    'r_ma': '红马',
    'r_xiang': '红相',
    'r_shi': '红仕',
    'r_jiang': '红帅'
}

replace_dict = {
    'r': 'r',
    'R': 'R',
    'n': 'n',
    'N': 'N',
    # 'k': 'n',
    # 'K': 'N',
    'b': 'b',
    'B': 'B',
    'a': 'a',
    'A': 'A',
    's': 'k',
    'S': 'K',
    'p': 'p',
    'P': 'P',
    'c': 'c',
    'C': 'C',
}

# replace_dict = {
#     'n': 'k',
#     'N': 'K',
#     'b': 'e',
#     'B': 'E',
#     'e': 'e',
#     'E': 'E',
#     'S': 'S',
#     's': 's',
#     'm': 'm',
#     'M': 'M',
#     'a': 'm',
#     'A': 'M',
#     'k': 'k',
#     'K': 'K',
#     # 'k': 's',
#     # 'K': 'S',
#     'r': 'r',
#     'R': 'R',
#     'p': 'p',
#     'P': 'P',
#     'c': 'c',
#     'C': 'C',
# }
state_to_board_dict = replace_dict
# state_to_board_dict = {
#     'k': 'n',
#     'K': 'N',
#     'e': 'b',
#     'E': 'B',
#     'm': 'a',
#     'M': 'A',
#     's': 'k',
#     'S': 'K',
#     'r': 'r',
#     'R': 'R',
#     'p': 'p',
#     'P': 'P',
#     'c': 'c',
#     'C': 'C',
# }

mov_dir = {
    'k': [(0, -1), (1, 0), (0, 1), (-1, 0)],
    'K': [(0, -1), (1, 0), (0, 1), (-1, 0)],
    'a': [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    'A': [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    'b': [(-2, -2), (2, -2), (2, 2), (-2, 2)],
    'B': [(-2, -2), (2, -2), (2, 2), (-2, 2)],
    'n': [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)],
    'N': [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)],
    'P': [(0, -1), (-1, 0), (1, 0)],
    'p': [(0, 1), (-1, 0), (1, 0)]}

bishop_check = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
knight_check = [(0, -1), (0, -1), (1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0)]


def get_kind(fen_ch):
    if fen_ch in ['k', 'K']:
        return KING
    elif fen_ch in ['a', 'A']:
        return ADVISOR
    elif fen_ch in ['b', 'B']:
        return BISHOP
    elif fen_ch in ['n', 'N']:
        return KNIGHT
    elif fen_ch in ['r', 'R']:
        return ROOK
    elif fen_ch in ['c', 'C']:
        return CANNON
    elif fen_ch in ['p', 'P']:
        return PAWN
    else:
        return NONE


def get_char(kind, color):
    if kind is KING:
        return ['K', 'k'][color]
    elif kind is ADVISOR:
        return ['A', 'a'][color]
    elif kind is BISHOP:
        return ['B', 'b'][color]
    elif kind is KNIGHT:
        return ['N', 'n'][color]
    elif kind is ROOK:
        return ['R', 'r'][color]
    elif kind is CANNON:
        return ['C', 'c'][color]
    elif kind is PAWN:
        return ['P', 'p'][color]
    else:
        return ''


def move_to_str(x, y, x_, y_):
    move_str = ''
    move_str += str(x)
    move_str += str(y)
    move_str += str(x_)
    move_str += str(y_)
    return move_str


def str_to_move(move_str):
    # move_str = move_str.replace("-", "")
    move_arr = [0] * 4
    move_arr[0] = int(move_str[0])
    move_arr[1] = int(move_str[1])
    move_arr[2] = int(move_str[2])
    move_arr[3] = int(move_str[3])
    return move_arr


class Move:
    def __init__(self, uci: str):
        s = str_to_move(uci)
        self.p = (s[0], s[1])
        self.n = (s[2], s[3])
        self.uci = uci

    @staticmethod
    def from_uci(uci):
        return Move(uci)
