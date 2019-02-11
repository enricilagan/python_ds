import string

alphanumeric_chars = list(string.ascii_letters + string.digits)


def get_index_different_char(chars):
    chars = [str(x) for x in chars]
    alpha = [x for x in chars if str(x) in alphanumeric_chars]
    non_alpha = [x for x in chars if str(x) not in alphanumeric_chars]
    if len(alpha) == 1:
        return chars.index(alpha[0])
    else:
        return chars.index(non_alpha[0])


def get_index_different_char(chars):
    matches, no_matches = [], []
    for i, char in enumerate(chars):  # iterate between index and item
        if str(char).lower() in alphanumeric_chars:
            matches.append(i)
        else:
            no_matches.append(i)
    return matches[0] if len(matches) == 1 else no_matches[0]

