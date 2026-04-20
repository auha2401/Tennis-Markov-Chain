from math import comb


def p_win_game(p: float) -> float:
    """
    Probability that a player wins a single game, given they win each point
    with probability p.

    A game ends when one side has at least 4 points and leads by 2. The
    calculation splits into two parts: winning before the score reaches deuce
    (3-3), and winning after reaching deuce. Once at deuce the game becomes a
    geometric series because every PQ or QP sequence returns to deuce, so only
    PP and QQ outcomes actually end the game.
    """
    q = 1 - p

    # Ways to win 4-0, 4-1, or 4-2. For a 4-k win we choose which k of the
    # first 3+k points go to the opponent, then win the final point.
    pre_deuce = sum(comb(3 + k, k) * p**4 * q**k for k in range(3))

    # Probability of reaching deuce at 3-3. Choose which 3 of the 6 points
    # played so far went to the opponent.
    p_deuce = comb(6, 3) * p**3 * q**3

    # Probability of eventually winning once at deuce. Derived by summing a
    # geometric series over the back and forth advantage cycles.
    p_win_deuce = p**2 / (p**2 + q**2) if (p**2 + q**2) > 0 else 0.5

    return pre_deuce + p_deuce * p_win_deuce


def p_win_tiebreak(p: float) -> float:
    """
    Probability of winning a tiebreak, given point win probability p.

    Same structure as a regular game but the target is 7 points instead of 4,
    still with a 2 point margin required. The formula mirrors p_win_game: sum
    of direct win paths, plus the probability of reaching 6-6 and winning the
    geometric series from there.
    """
    q = 1 - p

    # Direct wins from 7-0 through 7-5.
    pre_deuce = sum(comb(6 + k, k) * p**7 * q**k for k in range(6))

    # Probability of the tiebreak reaching 6-6.
    p_deuce = comb(12, 6) * p**6 * q**6

    # Same geometric series logic as deuce in a regular game.
    p_win_deuce = p**2 / (p**2 + q**2) if (p**2 + q**2) > 0 else 0.5

    return pre_deuce + p_deuce * p_win_deuce


def p_win_set(p: float) -> float:
    """
    Probability of winning a set, given point win probability p.

    First to 6 games wins, unless the score reaches 5-5, in which case a
    player can still win 7-5. At 6-6 a tiebreak decides the set.

    This is computed with dynamic programming over every possible game score
    (i, j), where i is the number of games our player has won and j is the
    opponent's. The recursion captures the Markov property directly: the
    probability of winning from any state depends only on pg (probability of
    winning a single game) and the probabilities from the two next states.
    """
    pg = p_win_game(p)
    ptb = p_win_tiebreak(p)
    memo: dict = {}

    def prob(i: int, j: int) -> float:
        # Return cached probability if this state has already been solved.
        if (i, j) in memo:
            return memo[(i, j)]

        # Terminal win states: 6-0 through 6-4, or 7-5.
        if (i == 6 and j <= 4) or (i == 7 and j == 5):
            result = 1.0
        # Terminal loss states, mirror of the win conditions.
        elif (j == 6 and i <= 4) or (j == 7 and i == 5):
            result = 0.0
        # At 6-6 the set is decided by a tiebreak.
        elif i == 6 and j == 6:
            result = ptb
        # Otherwise recurse: either we win the next game or the opponent does.
        else:
            result = pg * prob(i + 1, j) + (1 - pg) * prob(i, j + 1)

        memo[(i, j)] = result
        return result

    return prob(0, 0)


def p_win_match(p: float, best_of: int = 3) -> float:
    """
    Probability of winning a best of N match, given point win probability p.

    The first player to win ceil(N/2) sets takes the match. Uses the negative
    binomial formula: sum the probabilities of winning exactly the required
    number of sets while the opponent wins anywhere from 0 up to needed-1
    sets along the way.
    """
    ps = p_win_set(p)
    needed = (best_of + 1) // 2  # Sets required to clinch the match.

    total = 0.0
    for k in range(needed):
        # Probability of winning exactly `needed` sets with the opponent
        # winning k sets. The final set must be a win for us, so we arrange
        # the other k opponent wins among the first needed-1+k sets.
        total += comb(needed - 1 + k, k) * ps**needed * (1 - ps)**k
    return total
