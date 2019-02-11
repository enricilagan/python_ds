def rotate(string, n):
    """Rotate characters in a string. Expects string and n (int) for
       number of characters to move.
    """
    lst = list(string)
    if n > 0:
        for _ in range(n):
            lst.insert(len(lst), lst[0])
            lst.pop(0)
    if n < 0:
        for _ in range(-n):
            lst.insert(0, lst[len(lst) - 1])
            lst.pop(len(lst) - 1)
    return ''.join(lst)