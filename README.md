# Tennis Markov Chain

Analytical and simulation model for computing tennis match win probabilities using Markov chains.

Models the hierarchical structure of tennis scoring (points → games → sets → matches) with a single parameter `p`: the probability of winning any given point. Includes closed-form formulas for game and tiebreak probabilities, dynamic programming for set probabilities, and Monte Carlo simulation for validation.

## Usage

```bash
python main.py
```

## Structure

- `tennis_markov/analytical.py` — closed-form and DP probability calculations
- `tennis_markov/simulation.py` — point-by-point Monte Carlo simulation
- `tennis_markov/analysis.py` — tabular summaries and sensitivity analysis
- `main.py` — runs the full analysis
