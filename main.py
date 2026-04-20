#!/usr/bin/env python3
"""
Entry point for the analysis. Builds probability tables for best of 3 and
best of 5 formats, reports the sensitivity of match outcomes to point win
probability, and validates the analytical results against a Monte Carlo
simulation.
"""
from tennis_markov.analytical import p_win_match
from tennis_markov.simulation import run_simulation
from tennis_markov.analysis import build_table, print_table, derivative_at

# Range of point win probabilities to tabulate. Values close to 0.50 are
# included because that is where the amplification effect is most visible.
P_VALUES = [0.40, 0.45, 0.48, 0.50, 0.52, 0.55, 0.60]


def main():
    """Run the full analysis and print every result to stdout."""
    print("=" * 50)
    print("  TENNIS MARKOV CHAIN ANALYSIS")
    print("=" * 50)

    # Best of 3 sets (standard ATP and WTA tour matches).
    rows3 = build_table(P_VALUES, best_of=3)
    print_table(rows3, title="Best of 3 Sets")

    # Best of 5 sets (Grand Slam men's format).
    rows5 = build_table(P_VALUES, best_of=5)
    print_table(rows5, title="Best of 5 Sets")

    # Sensitivity shows how many percentage points the match win rate moves
    # for a one percentage point change in point win rate.
    print("\nSensitivity  dP(match)/dp  (best-of-3):")
    for p in [0.45, 0.50, 0.55]:
        dp = derivative_at(p, best_of=3)
        print(f"  p={p:.2f}:  {dp:.3f}")

    # Monte Carlo validation. With 100k trials the simulated value should be
    # within a few thousandths of the analytical value.
    print("\nMonte Carlo validation (p=0.55, best-of-3, 100k matches):")
    analytical = p_win_match(0.55, 3)
    simulated = run_simulation(0.55, n_matches=100_000, best_of=3, seed=42)
    print(f"  Analytical:  {analytical:.4f}")
    print(f"  Simulated:   {simulated:.4f}")
    print(f"  Difference:  {abs(analytical - simulated):.4f}")


if __name__ == "__main__":
    main()
