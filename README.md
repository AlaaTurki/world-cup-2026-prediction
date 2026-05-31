# WORLD CUP 2026 Predictor

A small Python project that scrapes the 2026 FIFA World Cup team list from Wikipedia (when available), estimates team features from Elo-based rankings, and visualizes win probability and scoring metrics.

## Features

- Scrape 2026 World Cup team data from Wikipedia
- Fall back to a static team list if scraping fails
- Estimate team statistics using Elo-style ratings
- Compute and display win probabilities
- Plot results with Matplotlib

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- requests
- beautifulsoup4

## Setup

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
```

2. Activate the environment:

- Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- Windows (CMD):
  ```cmd
  .venv\Scripts\activate.bat
  ```

3. Install dependencies:

```bash
python -m pip install pandas numpy matplotlib requests beautifulsoup4
```

## Usage

Run the script from the repository root:

```bash
python script.py
```

The script will attempt to scrape the team list from Wikipedia and print the top predicted teams by win probability. It will also display plots for win probability, estimated goals scored, and attack vs defense.

## Notes

- If internet access is unavailable or scraping fails, the script uses a predefined fallback team list.
- The model is a simple heuristic based on team Elo ratings and is intended for demonstration purposes only.

## License

This repository does not include a specific license file. Add one if you want to clarify reuse terms.
