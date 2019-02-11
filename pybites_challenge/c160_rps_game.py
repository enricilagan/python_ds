import csv
import os
from urllib.request import urlretrieve

BATTLE_DATA = os.path.join('/tmp', 'battle-table.csv')
if not os.path.isfile(BATTLE_DATA):
    urlretrieve('https://bit.ly/2U3oHft', BATTLE_DATA)

PLAYER = ['Rock', 'Gun', 'Lightning', 'Devil', 'Dragon', 'Water',
          'Air', 'Paper', 'Sponge', 'Wolf', 'Tree', 'Human', 'Snake', 'Scissors', 'Fire']


def _create_defeat_mapping():
    """Parse battle-table.csv building up a defeat_mapping dict
       with keys = attackers / values = who they defeat.
    """
    lst = []

    with open(BATTLE_DATA, encoding='utf-8') as f:
        for line in f:
            lst.append(line.strip().split(','))

    choices = lst[0][1:16]
    defeat_list = []
    for x in range(1, 16):
        defeat = []
        for y in range(1, 16):
            if lst[x][y] == 'win':
                defeat.append(choices[y - 1])
        defeat_list.append(defeat)

    defeat_mapping = {
        choices[0]: defeat_list[0],
        choices[1]: defeat_list[1],
        choices[2]: defeat_list[2],
        choices[3]: defeat_list[3],
        choices[4]: defeat_list[4],
        choices[5]: defeat_list[5],
        choices[6]: defeat_list[6],
        choices[7]: defeat_list[7],
        choices[8]: defeat_list[8],
        choices[9]: defeat_list[9],
        choices[10]: defeat_list[10],
        choices[11]: defeat_list[11],
        choices[12]: defeat_list[12],
        choices[13]: defeat_list[13],
        choices[14]: defeat_list[14]
    }

    return defeat_mapping


def get_winner(player1, player2, defeat_mapping=None):
    """Given player1 and player2 determine game output returning the
       appropriate string:
       Tie
       Player1
       Player2
       (where Player1 and Player2 are the names passed in)

       Raise a ValueError if invalid player strings are passed in.
    """
    if (player1 not in PLAYER) or (player2 not in PLAYER):
        raise ValueError

    defeat_mapping = defeat_mapping or _create_defeat_mapping()
    if player1 == player2:
        return 'Tie'
    elif player2 in defeat_mapping[player1]:
        return player1
    else:
        return player2


# Solution

import csv
import os
from urllib.request import urlretrieve

BATTLE_DATA = os.path.join('/tmp', 'battle-table.csv')
if not os.path.isfile(BATTLE_DATA):
    urlretrieve('https://bit.ly/2U3oHft', BATTLE_DATA)


def _create_defeat_mapping():
    """Parse battle-table.csv building up a defeat_mapping dict
       with keys = attackers / values = who they defeat.
    """
    defeat_mapping = {}
    with open(BATTLE_DATA) as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            attacker = row.pop("Attacker")
            defeat_mapping[attacker] = set()
            for player, state in row.items():
                if player == attacker:
                    continue
                if state.lower().strip() == 'win':
                    defeat_mapping[attacker].add(player)
    return defeat_mapping


def get_winner(player1, player2, defeat_mapping=None):
    """Given player1 and player2 determine game output returning the
       appropriate string:
       Tie
       Player1
       Player2
       (where Player1 and Player2 are the names passed in)

       Raise a ValueError if invalid player strings are passed in.
    """
    defeat_mapping = defeat_mapping or _create_defeat_mapping()

    if player1 not in defeat_mapping or player2 not in defeat_mapping:
        raise ValueError

    if player1 == player2:
        return 'Tie'

    defeated_by_player1 = defeat_mapping[player1]

    return player1 if player2 in defeated_by_player1 else player2

