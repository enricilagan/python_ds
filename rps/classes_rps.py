import pandas as pd

options = pd.read_csv('../data/battle-table.csv', index_col=0)

rps = pd.DataFrame({'Rock': ['draw', 'win', 'lose'],
                    'Paper': ['lose', 'draw', 'win'],
                    'Scissors': ['win', 'lose', 'draw']})
rps.index = ['Rock', 'Paper', 'Scissors']


class Player:
    def __init__(self, name):
        self.name = name
        self.rolls = []
        self.wins = 0


# Accepts a data frame that contains win, draw and lose information of the RPS game
class Roll:
    def __init__(self, name):
        self.name = name

    def can_defeat(self, roll):
        if options[roll][self.name] == 'win':
            return True
        elif options[roll][self.name] == 'lose':
            return False
