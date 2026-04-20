from math import comb


def p_win_game(p: float) -> float:
    """
    Probability of winning a single game given point win probability p. Splits
    into winning before deuce and winning from deuce, where the deuce phase
    collapses to a geometric series p^2 / (p^2 + q^2).
    """
    q = 1 - p
    pre_deuce = sum(comb(3 + k, k) * p**4 * q**k for k in range(3))
    p_deuce = comb(6, 3) * p**3 * q**3
    p_win_deuce = p**2 / (p**2 + q**2) if (p**2 + q**2) > 0 else 0.5
    return pre_deuce + p_deuce * p_win_deuce


def p_win_tiebreak(p: float) -> float:
    """
    Probability of winning a tiebreak. Same structure as a game but first to
    7 points with a 2 point margin.
    """
    q = 1 - p
    pre_deuce = sum(comb(6 + k, k) * p**7 * q**k for k in range(6))
    p_deuce = comb(12, 6) * p**6 * q**6
    p_win_deuce = p**2 / (p**2 + q**2) if (p**2 + q**2) > 0 else 0.5
    return pre_deuce + p_deuce * p_win_deuce


def p_win_set(p: float) -> float:
    """
    Probability of winning a set, computed with dynamic programming over game
    scores (i, j). Terminal states handle 6-0 through 7-5 directly, and a
    tiebreak resolves the 6-6 state.
    """
    pg = p_win_game(p)
    ptb = p_win_tiebreak(p)
    memo: dict = {}

    def prob(i: int, j: int) -> float:
        if (i, j) in memo:
            return memo[(i, j)]
        if (i == 6 and j <= 4) or (i == 7 and j == 5):
            result = 1.0
        elif (j == 6 and i <= 4) or (j == 7 and i == 5):
            result = 0.0
        elif i == 6 and j == 6:
            result = ptb
        else:
            result = pg * prob(i + 1, j) + (1 - pg) * prob(i, j + 1)
        memo[(i, j)] = result
        return result

    return prob(0, 0)


def p_win_match(p: float, best_of: int = 3) -> float:
    """
    Probability of winning a best of N match using the negative binomial
    formula applied to set win probability.
    """
    ps = p_win_set(p)
    needed = (best_of + 1) // 2
    total = 0.0
    for k in range(needed):
        total += comb(needed - 1 + k, k) * ps**needed * (1 - ps)**k
    return total
