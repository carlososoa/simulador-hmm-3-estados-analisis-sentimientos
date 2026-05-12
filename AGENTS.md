# Markov Sentiment Simulator

Spanish-language Pygame desktop app simulating a Hidden Markov Model (HMM) for social media sentiment analysis. 3 hidden states (Positivo, Neutral, Negativo) with 3 observation types.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Architecture (MVC)

- `model/hmm.py` — `HMM` class with 3×3 transition/emission matrices and a `generate_sequence()` method that returns a `SimulationResult`
- `view/` — 6 pygame screens (`TitleScreen` → `ConfigScreen` → `SimulationScreen` → `SummaryScreen` → `TrendScreen` → `StationaryScreen`)
- `controller/game.py` — `GameController` owns the pygame loop, screen stack, and HMM instance; `switch_to(i)` transitions between screens
- `words.py` — tweet template + word list generator (Spanish)
- `graphs.py` — matplotlib charts rendered to pygame surfaces via `fig_to_surface()` (uses `Agg` backend)

## Key conventions

- **Spanish UI** — all labels, tweets, and screen text are in Spanish
- **No tests, no CI, no linter/formatter config** — no pre-commit hooks, no type checking
- **Matplotlib charts** are created with dark theme (`#1a2036` background); call `plt.close(fig)` after converting to surface
- **Config screen** lets users edit matrices A, B, and π before simulation; defaults are hardcoded in `HMM.__init__()`
- **Simulation animates** at a rate depending on tweet count (10 → 300ms, 100 → 40ms, 500 → 5ms); scrollable tweet list
- **Stationary screen** shows the limit distribution converging via powers of A; references Perron-Frobenius theorem
