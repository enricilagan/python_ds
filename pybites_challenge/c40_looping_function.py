def _get_midpoint(start, stop):
    mid = (stop - start) / 2
    return 1 if mid == 0.5 else int(mid)


def binary_search(sequence, target, select=0, start=None, stop=None):
    if not start and not stop:
        start = 0
        stop = len(sequence) - 1
        select = _get_midpoint(start, stop)

    if sequence[select] == target:
        return select
    elif select == start == stop:
        return None

    start = select + 1 if sequence[select] < target else start
    stop = select if sequence[select] > target else stop
    change = _get_midpoint(start, stop)

    if change == 0 and sequence[start] == target:
        return start

    select += change if sequence[select] < target else change * -1
    return binary_search(sequence, target, select, start, stop)


def binary_search_alt(sequence, target):
    first = 0
    last = len(sequence) - 1
    found = False

    if type(sequence[0]) == str:
        sequence = [ord(x) - 96 for x in sequence]
        target = ord(target) - 96

    while first <= last and not found:
        midpoint = (first + last) // 2
        if sequence[midpoint] == target:
            found = True
        else:
            if target > sequence[midpoint]:
                if first == midpoint - 1:
                    first = midpoint
                elif first == midpoint:
                    first = midpoint + 1
                else:
                    first = midpoint - 1
            elif target < sequence[midpoint]:
                if last == midpoint + 1:
                    last = midpoint
                elif last == midpoint:
                    last = midpoint - 1
                else:
                    last = midpoint + 1

    if found:
        return midpoint
    else:
        return None
