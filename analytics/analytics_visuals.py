# analytics_visuals.py
import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ANALYTICS_FILE = Path(os.getenv("ANALYTICS_FILE", "analytics/events.jsonl"))
CHART_DIR = Path("charts")
CHART_DIR.mkdir(parents=True, exist_ok=True)

if not ANALYTICS_FILE.exists():
    raise SystemExit(f"Missing analytics file: {ANALYTICS_FILE}")

# ---------- Load ----------
df = pd.read_json(ANALYTICS_FILE, lines=True)
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"])
else:
    raise SystemExit("No 'timestamp' field found in events.")

# ---------- Time-series: queries per day ----------
# Filter interaction events
inter = df[df["type"] == "interaction"].copy()
if not inter.empty:
    inter = inter.set_index("timestamp").sort_index()
    daily = inter.resample("D").size()

    plt.figure()
    daily.plot()
    plt.title("Preparedness Queries per Day")
    plt.xlabel("Date")
    plt.ylabel("Queries")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "frequency_over_time.png")
    plt.close()
else:
    print("No interaction events yet; skipping time-series chart.")

# ---------- Funnel: impressions -> clicks -> purchases ----------
impr = df[df["type"] == "affiliate_impressions"]["count"].sum() if "count" in df.columns else 0
clicks = len(df[df["type"] == "affiliate_click"])
purch = len(df[df["type"] == "affiliate_purchase"])

funnel_labels = ["Impressions", "Clicks", "Purchases"]
funnel_vals = [int(impr), int(clicks), int(purch)]

plt.figure()
plt.bar(funnel_labels, funnel_vals)
plt.title("Affiliate Conversion Funnel")
plt.ylabel("Count")
for i, v in enumerate(funnel_vals):
    plt.text(i, v, str(v), ha="center", va="bottom")
plt.tight_layout()
plt.savefig(CHART_DIR / "affiliate_funnel.png")
plt.close()

# ---------- Heatmap: category frequency ----------
cat_source = inter if not inter.empty else df[df["type"] == "interaction"]
if not cat_source.empty and "category" in cat_source.columns:
    cat_counts = cat_source["category"].fillna("uncategorized").value_counts().sort_values(ascending=False)
    # reshape to a 1-row heatmap
    plt.figure()
    sns.heatmap(cat_counts.to_frame().T, annot=True, fmt="d")
    plt.title("Most Common Preparedness Topics (by Category)")
    plt.yticks([], [])  # hide single row label
    plt.tight_layout()
    plt.savefig(CHART_DIR / "topic_heatmap.png")
    plt.close()
else:
    print("No categories to plot; skipping heatmap.")

# ---------- Quick summary table (optional CSV) ----------
summary = pd.DataFrame({
    "metric": ["daily_points", "impressions", "clicks", "purchases"],
    "value": [int(len(inter.resample('D').size())) if not inter.empty else 0,
              int(impr), int(clicks), int(purch)]
})
summary.to_csv(CHART_DIR / "summary.csv", index=False)

print("✅ Charts written to ./charts/:")
print(" - frequency_over_time.png")
print(" - affiliate_funnel.png")
print(" - topic_heatmap.png")
print(" - summary.csv")

