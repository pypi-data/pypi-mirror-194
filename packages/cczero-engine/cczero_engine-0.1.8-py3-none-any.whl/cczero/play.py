# -*- coding:utf-8 -*-
import os
from collections import defaultdict
from logging import getLogger
from cczero.model import CChessModel
from cczero.player import CChessPlayer, VisitState
from cchess import BLACK, Move
from cczero.model_helper import load_best_model_weight
from cczero.env import CChessEnv

log = getLogger(__name__)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class Manager(object):
    @staticmethod
    def init(config):
        return PlayWithHuman(config).start()


class PlayWithHuman(object):
    def __init__(self, config):
        self.env = CChessEnv()
        self.config = config
        self.history = []
        self.model = None
        self.pipe = None
        self.nn_value = 0
        self.mcts_moves = []
        self.human_move_first = False
        self.ai = None
        super(PlayWithHuman).__init__()

    def load_model(self):
        self.model = CChessModel(self.config)
        self.model = CChessModel(self.config)
        if self.config.opts.new or not load_best_model_weight(self.model):
            self.model.build()

    def start(self, human_first=False):
        self.env.reset()
        self.load_model()
        self.human_move_first = human_first
        self.pipe = self.model.get_pipes(need_reload=False)
        self.ai = CChessPlayer(self.config, search_tree=defaultdict(VisitState), pipes=self.pipe, enable_resign=True, debugging=True, uci=False)
        return self

    def move(self):
        state = self.env.get_state()
        self.ai.search_results = {}
        if len(self.history) == 0:
            self.history.append(state)
        log.info(f"state = {state}")
        # if self.env.board.is_loss():
        #     self.env.winner = self.env.board.next_turn().__str__()
        #     return False, None, None
        no_act = []
        for step in self.env.board.create_moves():
            if self.env.board.is_checked_move(pos_from=step[0], pos_to=step[1]):
                no_act.append(self.env.board.tuple_to_str(step))
        # if not self.env.board.has_attack_chessman(state=state):
        #     self.env.winner = PLAYER[0]
        #     return False, None, None, None, state, self.env.winner
        # free_move[state] += 1
        # if free_move[state] >= 5:
        #     self.env.winner = PEACE
        #     return False, None, None, None, state, self.env.winner
        self.mcts_moves.clear()
        action, policy = self.ai.action(state=state, turns=self.env.num_halfmoves, no_act=no_act)
        if action is None:
            log.info("AI has resigned!")
            return False, None, None, self.mcts_moves
        if self.env.board.move_player == BLACK:
            action = self.env.board.flip_move(action)
        # log.info(f"{self.env.board.move_player} {action}")
        self.history.append(action)
        key = self.env.get_state()
        p, v = self.ai.debug[key]
        # log.info(f" NN value = {v:.3f}")
        self.nn_value = v
        for nominate, action_state in self.ai.search_results.items():
            try:
                if self.env.board.move_player == BLACK:
                    nominate = self.env.board.flip_move(nominate)
                pos_from, pos_to = self.env.board.str_to_move(action=nominate)
                move_cn = Move(self.env.board, pos_from, pos_to).to_chinese()
                self.mcts_moves.append([nominate, move_cn])
            except Exception as e:
                log.error(e)
        pos_from, pos_to = self.env.board.str_to_move(action=action)
        move = self.env.board.move(pos_from, pos_to)
        state = self.env.get_state()
        self.env.board.next_turn()
        return True, move, state, self.mcts_moves

    def close(self):
        self.ai.close(wait=True)
