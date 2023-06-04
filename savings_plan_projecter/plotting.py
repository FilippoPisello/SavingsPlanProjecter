from datetime import date

import matplotlib.dates as mdates
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def new_plot(
    title: str,
    subtitle: str,
    figsize: tuple[int, int] = (12, 5),
) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(top=0.88)
    fig.suptitle(
        title,
        fontsize=16,
        fontweight="bold",
        x=0.5,
        y=1,
        ha="center",
        va="top",
    )
    ax.set_title(subtitle, x=0.5, y=1.03, ha="center")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    return fig, ax


def cp_observation_period(df: pd.DataFrame) -> None:
    _, ax = new_plot(
        title="Splitting time between 2007 crisis and 'regular times' until Covid-19",
        subtitle="Daily closing value of S&P500 ($)",
        figsize=(12, 5),
    )

    observation_period = df.index.to_series().between("2007-01-01", "2020-12-01")
    ax.plot(
        pd.to_datetime(df[observation_period].index),
        df.loc[observation_period, "CLOSE"],
    )
    crisis_start_date = date(2007, 10, 10)
    crisis_end_date = date(2009, 3, 10)
    non_crisis_end_date = date(2020, 2, 1)

    ax.axvline(crisis_start_date, c="red", ls="dashed")
    ax.axvline(crisis_end_date, c="gray", ls="dashed")
    ax.axvline(non_crisis_end_date, c="green", ls="dashed")
    ax.axvspan(xmin=crisis_start_date, xmax=crisis_end_date, color="red", alpha=0.2)
    ax.axvspan(xmin=crisis_end_date, xmax=non_crisis_end_date, color="green", alpha=0.2)

    ax.text(
        x=date(2008, 3, 1),
        y=3250,
        s="Crisis",
        fontdict={"fontsize": 11, "color": "red"},
    )
    ax.text(
        x=date(2013, 12, 1),
        y=3250,
        s="Non-crisis",
        fontdict={"fontsize": 11, "color": "green"},
    )

    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.plot()


def cp_observation_period_crisis_only(df: pd.DataFrame) -> None:
    _, ax = new_plot(
        title="Setting narrow boundaries for the 2008 crisis",
        subtitle="Daily closing value of S&P500 ($)",
        figsize=(12, 5),
    )

    observation_period = df.index.to_series().between("2007-01-01", "2010-01-01")
    ax.plot(
        pd.to_datetime(df[observation_period].index),
        df.loc[observation_period, "CLOSE"],
    )
    crisis_start_date = date(2007, 10, 10)
    crisis_end_date = date(2009, 3, 10)

    ax.axvline(crisis_start_date, c="gray", ls="dashed")
    ax.axvline(crisis_end_date, c="gray", ls="dashed")
    ax.axvspan(xmin=crisis_start_date, xmax=crisis_end_date, color="gray", alpha=0.2)

    ax.text(
        x=date(2008, 10, 1),
        y=1550,
        s="Financial crisis",
        fontdict={"fontsize": 11, "color": "0.4"},
    )

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.plot()
