import random


def _point(p: float) -> int:
    """Simulate a single point. Returns 1 if the player wins it, 0 otherwise."""
    return 1 if random.random() < p else 0


def _game(p: float) -> int:
    """
    Simulate a full game point by point. Returns 1 if the player wins, 0
    otherwise, enforcing the 2 point lead requirement for deuce.
    """
    s, r = 0, 0
    while True:
        if _point(p):
            s += 1
        else:
            r += 1
        if s >= 4 and s - r >= 2:
            return 1
        if r >= 4 and r - s >= 2:
            return 0


def _tiebreak(p: float) -> int:
    """Simulate a tiebreak. First to 7 points with a 2 point margin wins."""
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
    Simulate a set by simulating games until one side reaches 6 with a 2 game
    lead, or until a tiebreak resolves a 6-6 score.
    """
    s, r = 0, 0
    while True:
        if _game(p):
            s += 1
        else:
            r += 1
        if s >= 6 and s - r >= 2:
            return 1
        if r >= 6 and r - s >= 2:
            return 0
        if s == 6 and r == 6:
            return _tiebreak(p)


def _match(p: float, best_of: int) -> int:
    """Simulate a best of N match by simulating sets until one side clinches."""
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
    won by the player. Seeded for reproducibility.
    """
    random.seed(seed)
    wins = sum(_match(p, best_of) for _ in range(n_matches))
    return wins / n_matches
