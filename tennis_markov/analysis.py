from typing import List, Tuple
from .analytical import p_win_game, p_win_set, p_win_match


def build_table(p_values: List[float], best_of: int = 3) -> List[Tuple[float, float, float, float]]:
    return [(p, p_win_game(p), p_win_set(p), p_win_match(p, best_of)) for p in p_values]


def print_table(rows: List[Tuple], title: str = "") -> None:
    if title:
        print(f"\n{title}")
    print(f"{'p':>6} | {'P(game)':>9} | {'P(set)':>9} | {'P(match)':>9}")
    print("-" * 43)
    for p, pg, ps, pm in rows:
        print(f"{p:>6.2f} | {pg:>9.4f} | {ps:>9.4f} | {pm:>9.4f}")


def derivative_at(p: float, best_of: int = 3, eps: float = 0.001) -> float:
    """Numerical derivative dP(match)/dp."""
    return (p_win_match(p + eps, best_of) - p_win_match(p - eps, best_of)) / (2 * eps)
