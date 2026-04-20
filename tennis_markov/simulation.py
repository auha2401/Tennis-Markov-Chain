import random


def _point(p: float) -> int:
    return 1 if random.random() < p else 0


def _game(p: float) -> int:
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
    needed = (best_of + 1) // 2
    s, r = 0, 0
    while s < needed and r < needed:
        if _set(p):
            s += 1
        else:
            r += 1
    return 1 if s == needed else 0


def run_simulation(p: float, n_matches: int = 100_000, best_of: int = 3, seed: int = 42) -> float:
    """Monte Carlo estimate of match win probability."""
    random.seed(seed)
    wins = sum(_match(p, best_of) for _ in range(n_matches))
    return wins / n_matches
