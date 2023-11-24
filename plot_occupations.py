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

    # get top n occupations
    data = data.sort_values(by = col, ascending=False).head(n)

    ax.barh(data.index.get_level_values("occupations"), data[col])

    ax.set_title(f"Top {n} occupations in {year}")

    ax.set_xlabel(col)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path / f"top_occupations_{year}_{col}.png")


if __name__ in "__main__":
    path = Path(__file__).parent

    # path to save figures to
    save_path = path / "fig"

    # ensure path exists
    if not save_path.exists():
        save_path.mkdir()

    # read in data
    data = pd.read_csv(path / "out" /"street_occupations.csv")

    # convert year to int
    data["year"] = data["year"].astype(int)

    for year in data["year"].unique():
        tmp_data = data[data["year"]==year]
        tmp_data = data.groupby(["occupations", "year"]).sum(numeric_only = True).sort_values("count", ascending=False)
        n_occupations = tmp_data.groupby("year").sum(numeric_only=True)["count"]
        tmp_data["rel_freq"] = tmp_data["count"]/n_occupations.values[0]

        most_common_occupations_year(tmp_data, year, n=30, col = "count", save_path = save_path)
        most_common_occupations_year(tmp_data, year, n=30, col = "rel_freq", save_path = save_path)


