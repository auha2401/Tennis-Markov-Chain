import random


def _point(p: float) -> int:
    """Simulate a single point. Returns 1 if the player wins it, 0 otherwise."""
    return 1 if random.random() < p else 0


def _game(p: float) -> int:
    """
    Simulate a full game point by point. Returns 1 if the player wins the
    game, 0 otherwise. Handles deuce automatically by requiring at least
    4 points and a 2 point lead.
    """
    s, r = 0, 0  # s is the player's points, r is the opponent's.
    while True:
        if _point(p):
            s += 1
        else:
            r += 1
        # Win condition: 4 or more points with a lead of at least 2.
        if s >= 4 and s - r >= 2:
            return 1
        if r >= 4 and r - s >= 2:
            return 0


def _tiebreak(p: float) -> int:
    """
    Simulate a tiebreak point by point. Same idea as _game but first to
    7 points wins, still requiring a 2 point margin.
    """
    s, r = 0, 0
    while True:
        if _point(p):
            s += 1
        else:
            r += 1
        if s >= 7 and s - r >= 2:
            return 1
        if r >= 7 and r - s >= 2:
            return 0


def _set(p: float) -> int:
    """
    Simulate a set by simulating games one at a time until a player reaches
    6 games with a 2 game lead, or until the set goes to a tiebreak at 6-6.
    """
    s, r = 0, 0
    while True:
        if _game(p):
            s += 1
        else:
            r += 1
        # Won outright anywhere from 6-0 through 7-5.
        if s >= 6 and s - r >= 2:
            return 1
        if r >= 6 and r - s >= 2:
            return 0
        # At 6-6 the set goes to a tiebreak.
        if s == 6 and r == 6:
            return _tiebreak(p)


def _match(p: float, best_of: int) -> int:
    """
    Simulate a best of N match by simulating sets until one side has won
    the required number.
    """
    needed = (best_of + 1) // 2
    s, r = 0, 0
    while s < needed and r < needed:
        if _set(p):
            s += 1
        else:
            r += 1
    return 1 if s == needed else 0


def run_simulation(p: float, n_matches: int = 100_000, best_of: int = 3, seed: int = 42) -> float:
    """
    Run a Monte Carlo simulation of n_matches matches and return the fraction
    won by the player. Used to sanity check the analytical results. The seed
    keeps the output reproducible across runs.
    """
    random.seed(seed)
    wins = sum(_match(p, best_of) for _ in range(n_matches))
    return wins / n_matches
