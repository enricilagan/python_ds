NAMES = ['arnold schwarzenegger', 'alec baldwin', 'bob belderbos',
         'julian sequeira', 'sandra bullock', 'keanu reeves',
         'julbob pybites', 'bob belderbos', 'julian sequeira',
         'al pacino', 'brad pitt', 'matt damon', 'brad pitt']


def dedup_and_title_case_names(names):
    """Should return a list of names, each name appears only once"""
    names = list(set(names))
    for x in range(len(names)):
        names[x] = names[x].title()
    return names


def sort_by_surname_desc(names):
    """Returns names list sorted desc by surname"""
    names = dedup_and_title_case_names(names)
    for x in range(len(names)):
        names[x] = names[x].split(' ')
    names.sort(key=lambda y: y[1], reverse=True)
    for x in range(len(names)):
        names[x] = names[x][0] + ' ' + names[x][1]
    return names


def shortest_first_name(names):
    """Returns the shortest first name (str)"""
    names = dedup_and_title_case_names(names)
    for x in range(len(names)):
        names[x] = names[x].split(' ')
        names[x].append(len(names[x][0]))
    names.sort(key=lambda y: y[2])
    return names[0][0]