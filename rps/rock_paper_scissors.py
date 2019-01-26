from classes_rps import Roll, Player, options
import random
# import os


def main():
    print_header()

    rolls = build_rolls()

    name = input('Please enter your name player 1: ')
    print()
    # Uses the player class to create players,right now it is still a 1-player only game
    player1 = Player(name)
    player2 = Player("Computer")
    print('{} is player1, fighting against {}'.format(player1.name, player2.name))
    rounds = input('How many rounds? Default is 3 ')
    if rounds is None:
        rounds = 3
    game_loop(player1, player2, rolls, int(rounds))


def print_header():
    print('------------------------------------')
    print('    This is a 15-way RPS game!')
    print('------------------------------------')
    print()


def build_rolls():
    """ Gets the list of possible rolls for the game, data is based on battle-table.csv.
    Stores all data in a list and then makes it accessible via index.
    """
    return [Roll(x) for x in list(options.index)]


def game_loop(player1, player2, rolls, rounds):
    count = 0
    winner = []
    # Loops while count is less than round, which is asked at the beginning of the game.
    while count < rounds:
        p2_roll = rolls[random.randint(0, (len(rolls)-1))]  # Randomizes between all possible options for rolls
        print('Are you ready? Choose between the following:')
        item = 0
        for x in rolls:
            print('[{}] - {}'.format(item+1, x.name))
            item += 1
        print()
        p1 = input('Enter the corresponding number for your choice? ')
        while int(p1) > len(rolls):
            p1 = input('You have selected a number not in the list choose again? ')
        print()
        p1_roll = rolls[int(p1)-1]

        # Prevents draw and will repeat the round if ever encountered.
        while p1_roll.name == p2_roll.name:
            print('{} and {} both chose {}. Repeat round {}!'.format(player1.name, player2.name, p2_roll.name, count+1))
            p2_roll = rolls[random.randint(0, len(rolls)-1)]
            p1 = input('Enter the corresponding number for your choice? ')
            while int(p1) > len(rolls):
                p1 = input('You have selected a number not in the list choose again? ')
            print()
            p1_roll = rolls[int(p1) - 1]

        player1.rolls.append(p1_roll.name)
        player2.rolls.append(p2_roll.name)
        outcome = p1_roll.can_defeat(p2_roll.name)  # Checks who won the game based on the battle-table data

        # display throws
        print('{} chose {}, {} chose {}'.format(player1.name, p1_roll.name, player2.name, p2_roll.name))

        # display winner for this round
        if outcome:
            print('{} beats {}, {} wins that round'.format(p1_roll.name, p2_roll.name, player1.name))
            print()
            player1.wins += 1
            winner.append(player1.name)

        else:
            print('{} beats {}, {} wins that round'.format(p2_roll.name, p1_roll.name, player2.name))
            print()
            player2.wins += 1
            winner.append(player2.name)
        count += 1

    # After all rounds, print out all the history of the rounds to summarize the game
    print('After {} round{}:'.format(rounds, 's' if rounds > 1 else ''))
    print()
    for x in range(count):
        print('Round {}: {} - {} vs. {} - {}, {} won this round.'.format(x+1, player1.name, player1.rolls[x],
                                                                         player2.name, player2.rolls[x], winner[x]))
    if player1.wins > player2.wins:
        winner = player1.name
    else:
        winner = player2.name

    print()
    # os.system('say "{} wins the game!"'.format(winner))
    print('{} wins the game!'.format(winner))


if __name__ == '__main__':
    main()
