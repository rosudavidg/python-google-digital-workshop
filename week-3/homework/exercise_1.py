def is_int(x):
    return isinstance(x, int)


def func(*args, **kwargs):
    return sum(filter(is_int, args))


x = 7
