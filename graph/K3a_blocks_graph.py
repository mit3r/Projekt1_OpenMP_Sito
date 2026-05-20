import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO

ranges_to_int = {
    "min_max": 10e8 - 2 + 1,
    "half_max": 10e8 - 10e8 // 2 + 1,
    "min_half": 10e8 // 2 - 2 + 1,
}

data = open("../outputs_4/k3a.csv", "r", encoding="utf-16").read()

df = pd.read_csv(
    StringIO(data),
    sep=';',
    header=0,
    names=["variant", "schedule", "chunk_size", "block_size", "range_name", "avg_time", "std_dev", "loops", "trials"],
    skipinitialspace=True,
)

df["avg_speed"] = df.apply(lambda row: (ranges_to_int.get(row["range_name"], None) * row["loops"] / row["avg_time"]) / 1e6, axis=1)

df["std_speed"] = df.apply(lambda row: row["std_dev"] / row["avg_time"] * row["avg_speed"], axis=1)

df["block_size_kb"] = df["block_size"].apply(lambda x: int(x) // 1024 if pd.notna(x) else None)

block_order = sorted(df['block_size_kb'].unique())
range_order = df['range_name'].drop_duplicates().tolist()
colors = {
    'min_max': '#1f77b4',
    'half_max': '#ff7f0e',
    'min_half': '#2ca02c',
}
display_labels = {
    'min_max': r'$[2, MAX]$',
    'half_max': r'$[\frac{MAX}{2}, MAX]$',
    'min_half': r'$[2, \frac{MAX}{2}]$',
}

fig, ax = plt.subplots(figsize=(12, 6), dpi=150)

x = np.arange(len(block_order))
bar_width = 0.22

for i, data_range in enumerate(range_order):
    sub_df = df[df['range_name'] == data_range].set_index('block_size_kb').reindex(block_order).reset_index()
    offset = (i - (len(range_order) - 1) / 2) * bar_width
    bars = ax.bar(
        x + offset,
        sub_df['avg_speed'],
        bar_width,
        yerr=sub_df['std_speed'],
        label=display_labels.get(data_range, data_range),
        color=colors.get(data_range, None),
        capsize=5,
        edgecolor='black',
        linewidth=0.5,
        error_kw={'elinewidth': 1.2},
    )

    ax.bar_label(
        bars,
        fmt='%.3f',
        padding=6,
        fontsize=9,
        weight='bold',
        color=colors.get(data_range, 'black'),
        rotation=90,
    )

ax.set_ylim(0, 10_000)
ax.set_xticks(x)
ax.set_xticklabels([f'{size:g} KB' for size in block_order], fontsize=10)

ax.set_title('Kod K3a - porównanie prędkości przetwarzania w zależności od rozmiaru bloku i zakresu danych', fontsize=14, pad=20, weight='bold')
ax.set_xlabel('Wielkość bloku [KB]', fontsize=12, labelpad=10)
ax.set_ylabel('Prędkość przetwarzania [Mliczb/s]', fontsize=12)

ax.grid(True, axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True)
ax.legend(
    title='Zakres danych',
    fontsize=11,
    title_fontsize=11,
    loc='upper right',
    # bbox_to_anchor=(0.5, 0.98),
    # ncol=len(range_order),
    borderaxespad=0.2,
)

plt.tight_layout()
#plt.show()
plt.savefig("../outputs_4/K3a.png")