"""Build the README / LinkedIn figures.

Run from the repository root:
    python scripts/make_figures.py

Uses only data/austin_311_model.csv (already in the repo). The model results
are copied from notebooks/Austin_311_Demand_Analysis.ipynb, where they are
computed.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)

INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#8a8984"
GRID = "#e6e5e1"
SURFACE = "#fcfcfb"
BLUE = "#2a78d6"
BLUE_LIGHT = "#a9c8ee"
ORANGE = "#eb6834"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def title(ax, text, sub):
    fig = ax.figure
    fig.text(0.03, 0.95, text, fontsize=15,
            fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.885, sub, fontsize=11,
            color=INK_2, va="top")


df = pd.read_csv(ROOT / "data" / "austin_311_model.csv", parse_dates=["date"])
# ---------------------------------------------------------------- Figure 1
yearly = df.groupby("year")["311_requests"].mean()
fig, ax = plt.subplots(figsize=(12, 5.6))
ax.plot(df.date, df["311_requests"].clip(upper=2500), color=BLUE_LIGHT, lw=0.8)
for yr, v in yearly.items():
    x0 = pd.Timestamp(f"{yr}-01-01")
    x1 = min(pd.Timestamp(f"{yr + 1}-01-01"), df.date.max())
    ax.plot([x0, x1], [v, v], color=BLUE, lw=2.5, solid_capstyle="round")
    ax.text(x0 + (x1 - x0) / 2, v + 70, f"{v:,.0f}", ha="center",
            fontsize=10, color=INK, fontweight="bold")
ax.annotate("Winter Storm Mara, Feb 2023\npeak 5,909 requests in one day (off chart)",
            xy=(pd.Timestamp("2023-02-06"), 2500), xytext=(pd.Timestamp("2019-09-01"), 2150),
            fontsize=10, color=INK_2,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=1))
ax.set_ylim(0, 2600)
ax.set_ylabel("Requests per day")
ax.grid(axis="y", color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.text(1, -0.12, "Light line: daily requests. Bold line + label: yearly daily average. "
        "Source: City of Austin Open Data (xwdj-i9he)",
        transform=ax.transAxes, ha="right", fontsize=9, color=MUTED)
title(ax, "Austin 311 now handles about twice the daily volume it did in 2018",
      "418 requests/day in 2018 to 819 in 2025. The jump came in 2023, and demand never went back down.")
fig.subplots_adjust(top=0.82, bottom=0.14, left=0.07, right=0.98)
fig.savefig(OUT / "demand_over_time.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- Figure 2
# Model results copied from the notebook (Stages 2-4, 2025 test period).
scores = [
    ("Multiple regression\n(lags + calendar + weather)", 262.5),
    ("Persistence\n(yesterday's value)", 180.7),
    ("Simple regression\n(yesterday's value)", 172.4),
]
fig, ax = plt.subplots(figsize=(11, 4.8))
labels = [x[0] for x in scores]
vals = [x[1] for x in scores]
colors = [ORANGE, "#c9c8c2", BLUE]
bars = ax.barh(labels, vals, color=colors, height=0.6)
for b, v in zip(bars, vals):
    ax.text(v + 4, b.get_y() + b.get_height() / 2, f"{v:.0f}", va="center",
            fontsize=11, color=INK, fontweight="bold")
ax.set_xlim(0, 300)
ax.set_xlabel("Average error per day, in requests (MAE, 2025). Lower is better.")
ax.grid(axis="x", color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
title(ax, "The most complex model did worst on unseen data",
      "Multiple regression explained 85% of demand in training (R² 0.85), but scored R² −0.49 on 2025.")
fig.subplots_adjust(top=0.78, bottom=0.15, left=0.24, right=0.97)
fig.savefig(OUT / "model_scoreboard.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- Figure 3
names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
wk = df.groupby("day_of_week")["311_requests"].mean()
fig, ax = plt.subplots(figsize=(9, 4.8))
bars = ax.bar(names, wk.values, color=[BLUE] * 5 + [BLUE_LIGHT] * 2, width=0.62)
for b, v in zip(bars, wk.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 12, f"{v:,.0f}", ha="center",
            fontsize=10, color=INK)
ax.set_ylabel("Average requests per day")
ax.grid(axis="y", color=GRID, lw=0.8)
ax.set_axisbelow(True)
title(ax, "Weekly rhythm: weekends get about 41% fewer requests",
      "Average daily requests by weekday, 2018 to Sep 2026")
fig.subplots_adjust(top=0.8, bottom=0.08, left=0.11, right=0.98)
fig.savefig(OUT / "weekday_pattern.png", dpi=200)
plt.close(fig)

print("Saved figures to", OUT)
