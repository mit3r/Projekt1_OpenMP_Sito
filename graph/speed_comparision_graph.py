import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO

ranges_to_int = {
    "min_max": 1e8 - 2 + 1,
    "half_max": 1e8 - 1e8 // 2 + 1,
    "min_half": 1e8 // 2 - 2 + 1,
}


data = open("../outputs/speed_comp.csv", "r", encoding="utf-16").read()


df = pd.read_csv(
    StringIO(data),
    sep=';',
    header=0,
    names=["variant", "schedule", "chunk_size", "block_size", "range_name", "avg_time", "std_dev", "loops", "trials"],
    skipinitialspace=True,
    keep_default_na=False,
)


df["variant"] = df["variant"].astype(str).str.strip()
df["range_name"] = df["range_name"].astype(str).str.strip()
for col in ["avg_time", "std_dev", "loops", "trials"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["avg_speed"] = df.apply(lambda row: (ranges_to_int.get(row["range_name"], None) * row["loops"] / row["avg_time"]) / 1e6, axis=1)
df["std_speed"] = df.apply(lambda row: row["std_dev"] / row["avg_time"] * row["avg_speed"], axis=1)

range_order = ['min_max', 'half_max', 'min_half']
colors = {'min_max': '#1f77b4', 'half_max': '#ff7f0e', 'min_half': '#2ca02c'}
display_labels = {
    'min_max': r'$[2, MAX]$',
    'half_max': r'$[\frac{MAX}{2}, MAX]$',
    'min_half': r'$[2, \frac{MAX}{2}]$',
}

variant_order = sorted(df['variant'].unique())

fig, ax = plt.subplots(figsize=(12, 6), dpi=150)

x = np.arange(len(variant_order))
bar_width = 0.25

for i, r_name in enumerate(range_order):
    sub_df = df[df['range_name'] == r_name].set_index('variant').reindex(variant_order).reset_index()
    
    pos = x + (i - 1) * bar_width
    
    bars = ax.bar(
        pos, sub_df['avg_speed'], bar_width, 
        yerr=sub_df['std_speed'],
        label=display_labels.get(r_name, r_name), color=colors[r_name],
        capsize=4, edgecolor='black', linewidth=0.5, error_kw={'elinewidth': 1.2}
    )

    ax.bar_label(
        bars, fmt='%.1f', padding=6, 
        fontsize=8.5, weight='bold', color=colors[r_name], rotation=45
    )

ax.set_yscale("log")
ax.set_ylim(0, max(df['avg_speed'] * 5))
ax.set_xticks(x)
ax.set_xticklabels(variant_order, fontsize=11, weight='bold')

ax.set_title('Porównanie prędkości przetwarzania wariantów kodu dla różnych zakresów danych', fontsize=14, pad=25, weight='bold')
ax.set_xlabel('Wariant kodu', fontsize=12, labelpad=10)
ax.set_ylabel('Prędkość przetwarzania [$10^6$ liczb/s]', fontsize=12)

ax.grid(True, axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True)

ax.legend(title='Zakres danych', fontsize=11, title_fontsize=11, loc='upper left')

plt.tight_layout()
plt.savefig("../outputs/speed_comp.png")