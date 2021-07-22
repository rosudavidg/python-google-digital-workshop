def sum_all(n):
    if n == 0:
        return 0

    return n + sum_all(n - 1)


def sum_evens(n):
    return 2 * sum_all(n // 2)
    # Or
    # return sum_evens_helper(n if n % 2 == 0 else n - 1)


def sum_evens_helper(n):
    if n == 0:
        return 0

    return n + sum_evens_helper(n - 2)


def sum_odds(n):
    return sum_odds_helper(n if n % 2 != 0 else n - 1)


def sum_odds_helper(n):
    if n < 0:
        return 0

    return n + sum_odds_helper(n - 2)
