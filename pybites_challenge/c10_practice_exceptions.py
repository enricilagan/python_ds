def positive_divide(numerator, denominator):
    if type(numerator) == str or type(denominator) == str:
        raise TypeError
    try:
        x = numerator/denominator
    except ZeroDivisionError:
        x = 0
    if x < 0:
        raise ValueError
    return x


print(positive_divide(1,'a'))