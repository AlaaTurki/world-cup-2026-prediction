import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None

WIKI_URL = 'https://en.wikipedia.org/wiki/2026_FIFA_World_Cup'

FALLBACK_TEAMS = [
    'Mexico', 'South Africa', 'South Korea', 'Czech Republic',
    'Canada', 'Bosnia and Herzegovina', 'Qatar', 'Switzerland',
    'Brazil', 'Morocco', 'Haiti', 'Scotland',
    'United States', 'Paraguay', 'Australia', 'Turkey',
    'Germany', 'Curaçao', 'Ivory Coast', 'Ecuador',
    'Netherlands', 'Japan', 'Sweden', 'Tunisia',
    'Belgium', 'Egypt', 'Iran', 'New Zealand',
    'Spain', 'Cape Verde', 'Saudi Arabia', 'Uruguay',
    'France', 'Senegal', 'Iraq', 'Norway',
    'Argentina', 'Algeria', 'Austria', 'Jordan',
    'Portugal', 'DR Congo', 'Uzbekistan', 'Colombia',
    'England', 'Croatia', 'Ghana', 'Panama'
]

TEAM_ELO = {
    'Argentina': 1850, 'France': 1845, 'Brazil': 1835, 'England': 1810,
    'Spain': 1795, 'Portugal': 1780, 'Netherlands': 1760, 'Germany': 1740,
    'Belgium': 1730, 'Croatia': 1710, 'Uruguay': 1705, 'Morocco': 1690,
    'Colombia': 1685, 'Ecuador': 1680, 'United States': 1670, 'Mexico': 1660,
    'Japan': 1650, 'Senegal': 1645, 'Canada': 1640, 'Switzerland': 1635,
    'Austria': 1625, 'South Korea': 1615, 'Turkey': 1605, 'Nigeria': 1600,
    'Ivory Coast': 1620, 'Australia': 1555, 'Norway': 1550,
    'Czech Republic': 1545, 'South Africa': 1530, 'Ghana': 1525,
    'Panama': 1515, 'Saudi Arabia': 1510, 'Qatar': 1505, 'Iraq': 1495,
    'Uzbekistan': 1490, 'Jordan': 1485, 'Haiti': 1470, 'Cape Verde': 1465,
    'DR Congo': 1460, 'Bosnia and Herzegovina': 1455, 'New Zealand': 1450,
    'Scotland': 1445, 'Curaçao': 1430
}

EXCLUDED_NAMES = {
    'AFC', 'CAF', 'CONCACAF', 'CONMEBOL', 'OFC', 'UEFA',
    'Qualification', 'Group', 'Teams'
}


def scrape_2026_world_cup_teams():
    """Scrape the 2026 World Cup team list from Wikipedia."""
    if requests is None or BeautifulSoup is None:
        raise ImportError('requests and beautifulsoup4 are required for scraping')

    response = requests.get(WIKI_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    teams = []
    for group_headline in soup.select('span.mw-headline'):
        headline = group_headline.text.strip()
        if not headline.startswith('Group '):
            continue

        table = group_headline.find_parent().find_next_sibling('table')
        if table is None:
            continue

        for row in table.select('tr')[1:]:
            cells = row.find_all(['th', 'td'])
            if len(cells) < 2:
                continue

            name_cell = cells[1]
            team_name = name_cell.get_text(strip=True)
            if not team_name or team_name in EXCLUDED_NAMES:
                continue

            if team_name not in teams:
                teams.append(team_name)

    if len(teams) >= 48:
        return teams

    return FALLBACK_TEAMS.copy()


def get_team_elo(team: str) -> int:
    return TEAM_ELO.get(team, 1500)


def estimate_team_features(team: str) -> dict:
    elo = get_team_elo(team)
    wins = max(5, min(18, int((elo - 1300) / 25) + 8))
    goals_scored = max(10, min(45, int((elo - 1200) / 20) + 18))
    goals_conceded = max(5, min(30, 40 - int((elo - 1200) / 30)))
    possession = max(38, min(70, int(52 + (elo - 1500) / 25)))
    return {
        'team': team,
        'wins': wins,
        'goals_scored': goals_scored,
        'goals_conceded': goals_conceded,
        'fifa_rank': elo,
        'possession': possession
    }


def build_dataframe(teams):
    rows = [estimate_team_features(team) for team in teams]
    return pd.DataFrame(rows)


def compute_win_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    score = (df['fifa_rank'] - df['fifa_rank'].mean()) / 100.0
    probability = 1 / (1 + np.exp(-score))
    df = df.copy()
    df['win_probability'] = probability
    return df.sort_values(by='win_probability', ascending=False)


def plot_results(df: pd.DataFrame):
    plt.figure(figsize=(14, 7))
    plt.bar(df['team'], df['win_probability'], color='tab:blue')
    plt.title('2026 World Cup Win Probability by Team')
    plt.xlabel('Team')
    plt.ylabel('Estimated Win Probability')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(14, 7))
    plt.plot(df['team'], df['goals_scored'], marker='o', linestyle='-')
    plt.title('Estimated Goals Scored')
    plt.xlabel('Team')
    plt.ylabel('Goals Scored')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 8))
    plt.scatter(df['goals_scored'], df['goals_conceded'], s=100, alpha=0.8)
    for _, row in df.iterrows():
        plt.text(row['goals_scored'] + 0.2, row['goals_conceded'] + 0.2, row['team'], fontsize=8)
    plt.title('Attack vs Defense')
    plt.xlabel('Goals Scored')
    plt.ylabel('Goals Conceded')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    try:
        teams = scrape_2026_world_cup_teams()
        print(f'Scraped {len(teams)} teams from the internet.')
    except Exception as exc:
        print(f'Could not scrape teams from the internet: {exc}')
        print('Using fallback World Cup teams list instead.')
        teams = FALLBACK_TEAMS.copy()

    df = build_dataframe(teams)
    df = compute_win_probabilities(df)  
    print(df[['team', 'win_probability']].head(20).to_string(index=False))
    plot_results(df)
