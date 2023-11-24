"""
This script plots the output from the count_occupations.py file
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def most_common_occupations_year(data, year, n=10, col = "n_freq", save_path = None):
    """
    plots the most common occupations for a given year
    
    Parameters
    ----------
    data : pd.DataFrame
        data frame containing the occupations
    year : int
        year to plot
    n : int, optional
        number of occupations to plot, by default 10
    col : str, optional
        column to to plot, by default "rel_freq"
    Returns
    -------
    None
    """
    fig, ax = plt.subplots(figsize = (8, 6), dpi = 300)

    # get data for given year
    data_year = data[data["year"] == year]

    # get top n occupations
    data_year = data_year.sort_values(by = col, ascending=False).head(n)

    ax.barh(data_year.index.get_level_values("occupations"), data_year[col])

    ax.set_title(f"Top {n} occupations in {year}")

    ax.set_xlabel(col)

    plt.tight_layout()

    if save_path:
        data_year.to_csv(save_path / f"top_occupations_{year}.csv")


if __name__ in "main":
    path = Path(__file__).parent

    # path to save figures to
    save_path = path / "fig"

    # ensure path exists
    save_path.mkdir(parents=True, exist_ok=True)

    # read in data
    data = pd.read_csv(path / "out" /"street_occupations.csv")

    # convert year to int
    data["year"] = data["year"].astype(int)

    for year in data["year"].unique():
        most_common_occupations_year(data, year, n=10, col = "n_freq", save_path = save_path)


