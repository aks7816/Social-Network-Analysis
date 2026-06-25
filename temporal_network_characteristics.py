import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from scipy.interpolate import make_interp_spline
from scipy.stats import pearsonr

# Load & prepare data
AIBD = pd.read_csv("LeidenNetworkBURSTDATACharacteristicsAIGlobal.csv")
AID  = pd.read_csv("LeidenNetworkDENSITYCharacteristicsAIGlobal.csv")
AIP  = pd.read_csv("LeidenNetworkPATHCharacteristicsAIGlobal.csv")
GNBD = pd.read_csv("LeidenNetworkBURSTDATACharacteristicsGN.csv")
GND  = pd.read_csv("LeidenNetworkDENSITYCharacteristicsGN.csv")
GNP  = pd.read_csv("LeidenNetworkPATHCharacteristicsGN.csv")

allAI = AIBD.merge(AIP, on="Year").merge(AID, on="Year")
allGN = GNBD.merge(GNP, on="Year").merge(GND, on="Year")
allAI.drop(["Unnamed: 0_x", 'Unnamed: 0_y', 'Unnamed: 0'], axis=1, inplace=True)
allGN.drop(["Unnamed: 0_x", 'Unnamed: 0_y', 'Unnamed: 0'], axis=1, inplace=True)

scaler = MinMaxScaler()
allAI_scaled = scaler.fit_transform(allAI[['Collabs', 'Path Length', 'Density']])
allGN_scaled = scaler.fit_transform(allGN[['Collabs', 'Path Length', 'Density']])

allAI_df = pd.DataFrame(allAI_scaled, columns=['Collabs', 'Path Length', 'Density'])
allAI_df["Year"] = allAI["Year"]
allAI_df = allAI_df[allAI_df["Year"] < 2025]

allGN_df = pd.DataFrame(allGN_scaled, columns=['Collabs', 'Path Length', 'Density'])
allGN_df["Year"] = allGN["Year"]

def plot_clean_trend_and_print_r(data_df, title):
    # Ensure sorted by Year
    data_df = data_df.dropna(subset=["Year"]).sort_values("Year").copy()
    x = data_df["Year"].to_numpy(dtype=float)

    r_values = {}

    plt.figure(figsize=(10, 6))
    for col, color in zip(["Density", "Path Length", "Collabs"],
                          ["#1f77b4", "#ff7f0e", "#2ca02c"]):
        y = data_df[col].to_numpy(dtype=float)

        # Smooth curve for visualization (safe k)
        try:
            x_smooth = np.linspace(x.min(), x.max(), 300)
            k = max(1, min(3, len(np.unique(x)) - 1))
            if k >= 1 and len(x) > k:
                spl = make_interp_spline(x, y, k=k)
                y_smooth = spl(x_smooth)
                plt.plot(x_smooth, y_smooth, color=color, linewidth=2.5, label=col)
            else:
                plt.plot(x, y, color=color, linewidth=2.0, label=col)
        except Exception:
            plt.plot(x, y, color=color, linewidth=2.0, label=col)

        # Trend line (simple linear fit)
        if len(x) >= 2:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), color=color, linestyle="--", linewidth=1.5, alpha=0.7)

        # Pearson r on raw (x, y)
        if np.std(x) == 0 or np.std(y) == 0:
            r, pval = np.nan, np.nan
        else:
            r, pval = pearsonr(x, y)
        r_values[col] = (r, pval)

        # Annotate r near the last year
        if not np.isnan(r):
            y_last = y[-1]
            plt.text(x.max(), y_last, f"  r={r:.2f}", color=color, va="center")


    plt.title(title, fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Normalized Metric", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Print a neat Pearson r table
    print(f"Pearson r for {title}:")
    for metric, (r, pval) in r_values.items():
        r_str = f"{r:.3f}" if not np.isnan(r) else "nan"
        p_str = f"{pval:.4g}" if not np.isnan(pval) else "nan"
        print(f"  {metric:<12}: r = {r_str},  p = {p_str}")
    print()


# ---- Plot Web Networking ----
plot_clean_trend_and_print_r(allGN_df, "WN")

# ---- Plot AI ----
plot_clean_trend_and_print_r(allAI_df, "AI")

