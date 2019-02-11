def transpose(data):
    """Transpose a data structure
    1. dict
    data = {'2017-8': 19, '2017-9': 13}
    In:  transpose(data)
    Out: [('2017-8', '2017-9'), (19, 13)]

    2. list of (named)tuples
    data = [Member(name='Bob', since_days=60, karma_points=60,
                   bitecoin_earned=56),
            Member(name='Julian', since_days=221, karma_points=34,
                   bitecoin_earned=78)]
    In: transpose(data)
    Out: [('Bob', 'Julian'), (60, 221), (60, 34), (56, 78)]
    """
    if isinstance(data, dict):
        return [data.keys(), data.values()]

    return list(zip(*data))


# Long cut
def transpose_long(data):
    lst = []
    if type(data) == dict:
        lst.append(tuple(data.keys()))
        lst.append(tuple(data.values()))
    elif type(data) == list:
        lst.append(tuple([x.name for x in data]))
        lst.append(tuple([x.since_days for x in data]))
        lst.append(tuple([x.karma_points for x in data]))
        lst.append(tuple([x.bitecoin_earned for x in data]))

    return lst
