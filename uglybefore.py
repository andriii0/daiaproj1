# Truly awful "pre-IBCS" style
fig, ax = plt.subplots(figsize=(16, 7))

# Random clashing colors and overlapping bars
ax.bar(df.index - 0.15, df["Actual_2024"], width=0.4, color='red', label="Actual 2024")
ax.bar(df.index + 0.0, df["Plan_2025"], width=0.4, color='green', label="Plan 2025")
ax.bar(df.index + 0.15, df["ActualForecast_2025"], width=0.4, color='blue', label="Actual/Forecast 2025")

# Numbers above bars (huge and overlapping)
for col, offset in zip(["Actual_2024", "Plan_2025", "ActualForecast_2025"], [-0.15, 0.0, 0.15]):
    for i, val in enumerate(df[col]):
        if not pd.isna(val):
            ax.text(i + offset, val + 30, f"{val:.0f}", ha="center", va="bottom", fontsize=12, color='brown', fontweight='bold')

# Messy X-axis
ax.set_xticks(df.index)
ax.set_xticklabels(df["Label"], rotation=30, ha="left", fontsize=10, color='darkblue')

# Ugly thick gridlines
ax.grid(True, which='both', axis='y', linestyle='--', linewidth=2, color='grey', alpha=0.7)
ax.grid(True, which='both', axis='x', linestyle='-.', linewidth=1, color='black', alpha=0.5)

# Oversized, centered title
ax.set_title("ALPHA CORPORATION — MONTHLY SALES VS PLAN!!!", fontsize=20, fontweight='heavy', color='darkred', loc='center')

# Y-axis label
ax.set_ylabel("Sales (€ millions)", fontsize=14, fontweight='bold', color='green')

# Ugly legend on top of bars
ax.legend(loc='upper center', fontsize=12, frameon=True, edgecolor='red')

plt.tight_layout()
plt.show()