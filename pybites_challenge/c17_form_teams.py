import itertools


def friends_teams(friends, team_size=2, order_does_matter=False):
    if order_does_matter:
        return list(itertools.permutations(friends, r=team_size))
    else:
        return list(itertools.combinations(friends, r=team_size))
