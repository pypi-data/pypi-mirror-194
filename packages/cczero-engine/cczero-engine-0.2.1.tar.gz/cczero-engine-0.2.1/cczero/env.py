from cchess import ChessBoard, FULL_INIT_FEN
from logging import getLogger

logger = getLogger(__name__)


class CChessEnv:

    def __init__(self, config=None):
        self.board = ChessBoard()
        self.winner = None
        self.num_halfmoves = 0
        self.config = config

    def reset(self, state=FULL_INIT_FEN):
        self.board.from_fen(state)
        self.winner = None
        self.num_halfmoves = 0
        return self

    @property
    def play_observation(self):
        return self.board.to_fen_base()

    def get_board_state(self):
        fen = self.play_observation
        foo = fen.split(' ')
        return foo[0]

    def get_state(self):
        fen = self.observation
        foo = fen.split(' ')
        return foo[0]

    @property
    def observation(self):
        if self.board.move_player.__str__() == 'RED':
            return self.play_observation
        else:
            return self.fliped_FENboard()

    @staticmethod
    def swapcase(a):
        if a.isalpha():
            return a.lower() if a.isupper() else a.upper()
        return a

    def swapall(self, aa):
        return "".join([self.swapcase(a) for a in aa])

    def fliped_FENboard(self):
        fen = self.board.to_fen()
        foo = fen.split(' ')
        rows = foo[0].split('/')
        return "/".join([self.swapall(reversed(row)) for row in reversed(rows)]) \
               + " " + ('r' if foo[1] == 'b' else 'b') \
               + " " + foo[2] \
               + " " + foo[3] + " " + foo[4] + " " + foo[5]
