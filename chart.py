# chart code
# will draw the CI bar and save it as an image

# chart.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def generate_chart(grouped_data=None):
    # Use sample data if no real data passed in
    if grouped_data is None or len(grouped_data) < 2:
        np.random.seed(42)
        grouped_data = {
            "Control": list(np.random.normal(30, 5, 10)),
            "Biostimulant A": list(np.random.normal(45, 6, 10))
        }

    groups = list(grouped_data.keys())
    means, cis = [], []

    for g in groups:
        values = grouped_data[g]
        mean = np.mean(values)
        ci = stats.sem(values) * 1.96
        means.append(round(mean, 2))
        cis.append(round(ci, 2))

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["steelblue", "darkgreen", "darkorange", "crimson"]
    bars = ax.bar(groups, means,
                  color=colors[:len(groups)],
                  width=0.4, yerr=cis, capsize=10,
                  error_kw={"linewidth": 2, "ecolor": "black", "capthick": 2})

    ax.set_title("95% Confidence Interval Comparison\nNitrate Level (mg/L)",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Nitrate Level (mg/L)", fontsize=12)
    ax.set_xlabel("Treatment Group", fontsize=12)

    for bar, mean, ci in zip(bars, means, cis):
        ax.text(bar.get_x() + bar.get_width() / 2,
                mean + ci + 0.5,
                f"Mean: {mean}\n±{ci}",
                ha="center", va="bottom",
                fontsize=10, fontweight="bold")

    ax.set_ylim(0, max(means) + max(cis) + 10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig("static/ci_chart.png", dpi=150, bbox_inches="tight")
    plt.close()



