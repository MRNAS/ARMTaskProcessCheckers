"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
from typing import Tuple
from typing import Dict
from typing import List
from types import SimpleNamespace
import numpy as np

from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.base import DarkPiece
from seoulai_gym.envs.checkers.base import LightPiece
from seoulai_gym.envs.checkers.rules import Rules
from seoulai_gym.envs.checkers.utils import generate_random_move


class Rewards(object):
    def __init__(self):
        self._rew = SimpleNamespace(
            moveback=-3,
            moveback1=-2,
            moveback2=-1,
            default=1.0,
            moveforward=2.0, #
            moveforward1=3.0,
            moveforward2=4.0,
            # smallmoves=5.0, #
            invalid_move=0.0,
            move_opponent_piece=0.0,
            remove_opponent_piece=5.0,
            become_king=20.0, #7
            opponent_no_pieces=0.0, #10.0
            opponent_no_valid_move=0.0, #20.0
        )

    def __getitem__(self, name: str):
        return self._get_reward(name)

    def __setitem__(self, name: str, value: float):
        # tests if reward exists, exception is not catched on purpose
        self._get_reward(name)
        return setattr(self._rew, name, value)

    def _get_reward(self, name: str):
        try:
            return getattr(self._rew, name)
        except AttributeError:
            raise AttributeError(f"[{name}] reward does not exists")


class Board(Constants, Rules):
    def __init__(
        self,
        size: int=8,
    ):
        """Board constructor.

        Args:
            size: Board size.
        """
        self.size = size
        self.init()
        self.rewards = Rewards()

    def init(
        self,
    ) -> None:
        """Initialize board and setup pieces on board.

        Note: Dark pieces should be ALWAYS on the top of the board.
        """
        half_size = self.size//2
        self.board_list = [
            # sum([[DarkPiece(), LightPiece()] for _ in range(4)], []),
            # sum([[DarkPiece(), None,None,None,None,LightPiece(),None,None] ], []),
            sum([[None] for _ in range(self.size)], []),
            sum([[None] for _ in range(self.size)], []),
            sum([[None, None, None,None,None,LightPiece(),None,None] ], []), ##two agents
            sum([[None, None, None,None,None,None,None,None] ], []), ##two agents
            # sum([[None, None,None,None,LightPiece(),None,None,None] ], []), ##one agents
            # sum([[DarkPiece(), None,None,None,None,LightPiece(),None,None] ], []),
            # sum([[DarkPiece(), None,None,None,None,LightPiece(),None,None] ], []),
            # sum([[DarkPiece(), None,None,None,None,LightPiece(),None,None] ], []),
            # sum([[None] for _ in range(self.size)], []),
            sum([[None] for _ in range(self.size)], []),
            sum([[None] for _ in range(self.size)], []),
            
            sum([[None] for _ in range(self.size)], []),
            sum([[None] for _ in range(self.size)], []),
        ]
        # self.board_list = [
        #     sum([[None, DarkPiece()] for _ in range(half_size)], []),
        #     sum([[DarkPiece(), None] for _ in range(half_size)], []),
        #     sum([[None, DarkPiece()] for _ in range(half_size)], []),
        #     sum([[None] for _ in range(self.size)], []),
        #     sum([[None] for _ in range(self.size)], []),
        #     sum([[LightPiece(), None] for _ in range(half_size)], []),
        #     sum([[None, LightPiece()] for _ in range(half_size)], []),
        #     sum([[LightPiece(), None] for _ in range(half_size)], []),
        # ]

    def update_rewards(
        self,
        rewards_map: Dict,
    ) -> None:
        """Update rewards. Adding new reward is not allowed.

        If `rewards_map` contains reward that wasn't defined in `Rewards`,
        AttributeError will be raised.

        Args:
            rewards_map: (Dict)

        Returns:
            None

        Raises:
            AttributeError: If attempts to add new reward.
        """
        for key, value in rewards_map.items():
            self.rewards[key] = value

    def move(
        self,
        ptype: int,
        from_row: int,
        from_col: int,
        to_row: int,
        to_col: int,
    ) -> Tuple[List[List], int, bool, Dict]:
        """Move piece across board and check validity of movement.

        Args:
            ptype: Type of piece making a move.
            from_row: Row of board of original piece location.
            from_col: Column of board of original piece location.
            to_row: Row of board of desired piece location.
            to_col: Column of board of desired piece location.

        Returns:
            obs: information about positions of pieces.
            rew: reward for perfomed step.
            done: information about end of game.
            info: additional information about current step.
        """
        rew = self.rewards["default"]
        info = {}
        done = False

        # if not self._can_opponent_move(self.board_list, self.get_opponent_type(ptype), self.size):
        #     print("condition1")
        #     return self._opponent_cant_move(self.board_list, self.rewards, info)

        # general invalid move
        # if not self.validate_move(self.board_list, from_row, from_col, to_row, to_col):
        #     rew = self.rewards["invalid_move"]
        #     info.update({"invalid_move": (from_row, from_col, to_row, to_col)})
        #     print("condition2")

        #     from_row, from_col, to_row, to_col = generate_random_move(
        #         self.board_list,
        #         ptype,
        #         self.size,
        #     )

        # don't move with opponent's piece
        # if ptype != self.board_list[from_row][from_col].ptype:
        #     rew = self.rewards["move_opponent_piece"]
        #     info.update({"move_opponent_piece": (from_row, from_col)})
        #     print("condition3")

        #     from_row, from_col, to_row, to_col = generate_random_move(
        #         self.board_list,
        #         ptype,
        #         self.size,
        #     )

        # move piece
        info_update = self.execute_move(from_row, from_col, to_row, to_col)
        # print(from_row, from_col, to_row, to_col)
        info.update(info_update)
        # print(info_update)

        # remove opponent's piece
        between_row, between_col = self.get_between_position(from_row, from_col, to_row, to_col)
        if between_row is not None and between_col is not None:
            print("condition4")
            p_between = self.board_list[between_row][between_col]
            if p_between is not None:
                self.board_list[between_row][between_col] = None
                info.update({"removed": ((between_row, between_col), p_between)})
                rew = self.rewards["remove_opponent_piece"]

        #move back penalty
        p = self.board_list[to_row][to_col]
        if (to_row == self.size-8 and p.direction == self.DOWN) or (to_row == self.size-4 and p.direction == self.UP):
            print("condition5")
            # p.make_king()
            # info.update({"winning": (to_row, to_col)})
            rew = self.rewards["moveback"]

        p = self.board_list[to_row][to_col]
        if (to_row == self.size-7 and p.direction == self.DOWN) or (to_row == self.size-4 and p.direction == self.UP):
            # p.make_king()
            info.update({"losing": (to_row, to_col)})
            rew = self.rewards["moveback1"]
        
        p = self.board_list[to_row][to_col]
        if (to_row == self.size-6 and p.direction == self.DOWN) or (to_row == self.size-4 and p.direction == self.UP):
            # p.make_king()
            info.update({"losing": (to_row, to_col)})
            rew = self.rewards["moveback2"]

        #move forward reward
        p = self.board_list[to_row][to_col]
        if (to_row == self.size-4 and p.direction == self.DOWN) or (to_row == self.size-4 and p.direction == self.UP):
            # p.make_king()
            info.update({"winning": (to_row, to_col)})
            rew = self.rewards["moveforward"]

        p = self.board_list[to_row][to_col]
        if (to_row == self.size-3 and p.direction == self.DOWN) or (to_row == self.size-3 and p.direction == self.UP):
            # p.make_king()
            info.update({"winning": (to_row, to_col)})
            rew = self.rewards["moveforward1"]
        
        p = self.board_list[to_row][to_col]
        if (to_row == self.size-2 and p.direction == self.DOWN) or (to_row == self.size-2 and p.direction == self.UP):
            # p.make_king()
            info.update({"winning": (to_row, to_col)})
            rew = self.rewards["moveforward2"]

        # become king wins
        p = self.board_list[to_row][to_col]
        # if (to_row == 0 and p.direction == self.UP) or (to_row == self.size-1 and p.direction == self.DOWN): #old
        if (to_row == self.size-1 and p.direction == self.DOWN) or (to_row == self.size-1 and p.direction == self.UP):
            p.make_king()
            info.update({"king": (to_row, to_col)})
            rew = self.rewards["become_king"]
            done = True

        # end of game?
        # if len(self.get_positions(self.board_list, self.get_opponent_type(p.ptype), self.size)) == 0:
        #     # opponent lost all his pieces
        #     # done = True #old
        #     done = False
        #     rew = self.rewards["opponent_no_pieces"]
        #     info.update({"opponent_no_pieces": True})
        done = False 
        # if not self._can_opponent_move(self.board_list, self.get_opponent_type(ptype), self.size):
        #     print("tacos")
        #     return self._opponent_cant_move(self.board_list, self.rewards, info)

        obs = self.board_list
        # print("tacos")
        # print(obs)
        return obs, rew, done, info

    def execute_move(
        self,
        from_row: int,
        from_col: int,
        to_row: int,
        to_col: int,
    ) -> Dict:
        # print(to_row,to_col)
        self.board_list[to_row][to_col] = self.board_list[from_row][from_col]
        self.board_list[from_row][from_col] = None
        return {"moved": ((from_row, from_col), (to_row, to_col))}

    @staticmethod
    def _can_opponent_move(
        board_list: List[List],
        opponent_ptype: int,
        board_size: int,
    ) -> bool:
        if len(Rules.generate_valid_moves(board_list, opponent_ptype, board_size)) == 0:
            return False
        else:
            return True

    @staticmethod
    def _opponent_cant_move(
        board_list: List[List],
        rewards: Rewards,
        info: Dict,
    ) -> Tuple[List[List], int, bool, Dict]:
        obs = board_list
        rew = rewards["opponent_no_valid_move"]
        info.update({"opponent_invalid_move": True})
        # done = True
        done = False
        return obs, rew, done, info
