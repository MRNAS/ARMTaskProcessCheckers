"""
Requires pytest
https://pytest.org/

Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
import pytest

from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.board import Board
from seoulai_gym.envs.checkers.board import DarkPiece
from seoulai_gym.envs.checkers.board import LightPiece
from seoulai_gym.envs.checkers.rules import Rules


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def dark():
    return Constants().DARK


@pytest.fixture
def light():
    return Constants().LIGHT


@pytest.fixture
def empty_board():
    board = Board()
    board.board_list = [[None] * board.size] * board.size
    return board


class TestInvalidMoves(object):
    def test_jump_from_non_jump_position(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 0, 0, 3, 3)

    def test_jump_from_non_jump_to_no_jump_position(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 0, 0, 2, 2)

    def test_no_move(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 0, 0, 0, 0)

    def test_invalid_from_coord(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, -1, -1, 0, 0)

    def test_invalid_to_coord(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 0, 0, -1, -1)

    def test_move_empty_square(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 0, 1, 1, 2)

    def test_move_in_opposite_direction(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 0, 1, 1, 2)

    def test_jump_over_empty_square(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 2, 0, 4, 2)

    def test_jump_with_opponents_dark_piece(self, board, light):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 3, 3, 4, 4)

    def test_jump_with_opponents_light_piece(self, board, dark):
        with pytest.raises(ValueError):
            obs, rew, done, info = board.move(dark, 6, 6, 5, 5)


class TestRemove(object):
    def test_jump_dark_forward(self, empty_board, dark):
        empty_board.board_list[3][3] = DarkPiece()
        light = LightPiece()
        empty_board.board_list[4][4] = light
        obs, rew, done, info = empty_board.move(dark, 3, 3, 5, 5)

        assert info["removed"] == ((4, 4), light)
        assert info["moved"] == ((3, 3), (5, 5))
        assert empty_board.board_list[4][4] is None
        assert done

    def test_jump_light_forward(self, empty_board, light):
        dark = DarkPiece()
        empty_board.board_list[3][3] = dark
        empty_board.board_list[4][4] = LightPiece()
        obs, rew, done, info = empty_board.move(light, 4, 4, 2, 2)

        assert info["removed"] == ((3, 3), dark)
        assert info["moved"] == ((4, 4), (2, 2))
        assert empty_board.board_list[3][3] is None
        assert done


class TestEndOfGame(object):
    def test_no_piece(self, empty_board, dark):
        empty_board.board_list[0][0] = DarkPiece()
        obs, rew, done, info = empty_board.move(dark, 0, 0, 1, 1)
        assert done

    def test_no_possible_jump(self, empty_board, light):
        """
        X - -        X - -
        - - -   ->   - O -
        O - 0        - - 0
        """
        empty_board.board_list[0][0] = DarkPiece()

        empty_board.board_list[2][2] = LightPiece()
        empty_board.board_list[2][0] = LightPiece()

        obs, rew, done, info = empty_board.move(light, 2, 0, 1, 1)
        assert done


class TestRules(object):
    def test_get_between_position(self):
        rules = Rules()
        # UP LEFT
        assert rules.get_between_position(4, 4, 3, 3) == (None, None)
        assert rules.get_between_position(4, 4, 2, 2) == (3, 3)

        # UP RIGHT
        assert rules.get_between_position(4, 4, 3, 5) == (None, None)
        assert rules.get_between_position(4, 4, 2, 6) == (3, 5)

        # DOWN LEFT
        assert rules.get_between_position(4, 4, 5, 3) == (None, None)
        assert rules.get_between_position(4, 4, 6, 2) == (5, 3)

        # DOWN RIGHT
        assert rules.get_between_position(4, 4, 5, 5) == (None, None)
        assert rules.get_between_position(4, 4, 6, 6) == (5, 5)


class TestInitialization(object):
    def test_board_init(self):
        B = Board(size=8)
        assert len(set(sum(B.board_list, []))) == 1 + (4 + 4 + 4) * 2
