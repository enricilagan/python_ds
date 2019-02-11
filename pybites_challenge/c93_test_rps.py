from unittest.mock import patch

import pytest

from code import (_get_winner, game, lose, win, tie)


@pytest.fixture()
def my_game():
    """Initialize game and move it to point where to
       receive first player (send) input"""
    gen = game()
    next(gen)
    return gen


@patch('code._get_computer_move')
def test_win(computerMoveMock, my_game, capfd):
    computerMoveMock.return_value = 'rock'
    my_game.send('paper')
    output = capfd.readouterr()[0].strip()
    assert output == win.format('paper', 'rock')


@patch('code._get_computer_move')
def test_loose(computerMoveMock, my_game, capfd):
    computerMoveMock.return_value = 'rock'
    my_game.send('scissors')
    output = capfd.readouterr()[0].strip()
    assert output == lose.format('rock', 'scissors')


@patch('code._get_computer_move')
def test_tie(computerMoveMock, my_game, capfd):
    computerMoveMock.return_value = 'paper'
    my_game.send('paper')
    output = capfd.readouterr()[0].strip()
    assert output == tie


def test_get_winner():
    # _get_winner takes computer then player choice
    assert 'lose' in _get_winner('scissors', 'paper')
    assert 'win' in _get_winner('paper', 'scissors')
    assert 'win' in _get_winner('rock', 'paper')
    assert 'lose' in _get_winner('paper', 'rock')
    assert 'lose' in _get_winner('rock', 'scissors')
    assert 'win' in _get_winner('scissors', 'rock')


def test_stop_iteration(my_game):
    # 3.6 = StopIteration
    # 3.7 = RuntimeError - see: https://bugs.python.org/issue32670
    with pytest.raises((StopIteration, RuntimeError)):
        my_game.send('q')