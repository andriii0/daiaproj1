import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# IBCS style colors
COL = {
    "actual": "black",
    "forecast": "white",
    "forecast_edge": "black",
    "plan": "white",
    "plan_edge": "grey",
    "prev": "#d3d3d3",
}

# Generate months (Jan 2024 – Dec 2025)
months = pd.date_range("2024-01-01", "2025-12-01", freq="MS")
labels = [m.strftime("%b\n%Y") for m in months]

# Fake data
np.random.seed(42)
actual_2024 = np.random.randint(500, 1000, 12)
actual_2025 = np.random.randint(500, 1000, 3)     # Jan–Mar actual
forecast_2025 = np.random.randint(500, 1000, 9)   # Apr–Dec forecast
plan_2025 = np.random.randint(550, 950, 12)       # Plan for all 12 months

# Dataframe
df = pd.DataFrame({"Month": months, "Label": labels})
df["Actual_2024"] = [*actual_2024, *[np.nan]*12]
df["Actual_2025"] = [np.nan]*12 + list(actual_2025) + [np.nan]*9
df["Forecast_2025"] = [np.nan]*12 + [np.nan]*3 + list(forecast_2025)
df["Plan_2025"] = [np.nan]*12 + list(plan_2025)

# Merge actual + forecast
df["ActualForecast_2025"] = df["Actual_2025"].combine_first(df["Forecast_2025"])
df["AbsVar"] = df["ActualForecast_2025"] - df["Plan_2025"]
df["RelVarPct"] = df["AbsVar"] / df["Plan_2025"] * 100

# Plot
fig, ax = plt.subplots(figsize=(16, 7))

bar_width = 0.625          # thick main bars
plan_width = 0.35       # same width as main bars for overlay
plan_shift = -0.3       # shift Plan bar left by 0.2 (half bar width)

# Offsets
offsets = {
    "Actual_2024": -1.0 * bar_width,
    "Plan_2025": plan_shift,       # move Plan to left so it’s behind Actual/Forecast
    "Forecast_2025": 0.2,
    "Actual_2025": 0.18
}

# Plot bars
ax.bar(df.index + offsets["Actual_2024"], df["Actual_2024"], width=bar_width,
       color=COL["prev"], label="Actual 2024")

ax.bar(df.index + offsets["Plan_2025"], df["Plan_2025"], width=plan_width,
       facecolor=COL["plan"], edgecolor=COL["plan_edge"], label="Plan 2025")

ax.bar(df.index + offsets["Forecast_2025"], df["Forecast_2025"], width=bar_width,
       facecolor=COL["forecast"], edgecolor=COL["forecast_edge"], hatch="///", label="Forecast 2025")

ax.bar(df.index + offsets["Actual_2025"], df["Actual_2025"], width=bar_width,
       color=COL["actual"], label="Actual 2025")

# Numbers above bars
for col, offset in offsets.items():
    width = plan_width if col == "Plan_2025" else bar_width
    for i, val in enumerate(df[col]):
        if not pd.isna(val):
            ax.text(i + offset, val + 15, f"{val:.0f}",
                    ha="center", va="bottom", fontsize=8)

# Labels & formatting
ax.set_xticks(df.index)
ax.set_xticklabels(df["Label"], rotation=45, ha="right")

# Title smaller + left-aligned
ax.set_title("Alpha Corporation — Monthly Sales vs Plan (Overlay Style)",
             fontsize=11, weight="bold", loc="left")

ax.set_ylabel("Sales (€ millions)")
ax.set_ylim(bottom=0)
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
ax.grid(axis="y", linestyle=":", linewidth=0.5, color="grey", alpha=0.5)

# Clean frame
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend
ax.legend(loc="upper left")

plt.tight_layout()
plt.show()