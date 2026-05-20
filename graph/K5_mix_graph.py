import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = open("../outputs/k5.csv", "r", encoding="utf-16").read()

from io import StringIO
df = pd.read_csv(
    StringIO(data),
    sep=';',
    header=0,
    names=["name", "type", "chunk_size", "block_size", "range_name", "time", "std", "loops", "trials"],
    skipinitialspace=True,
)

df['type'] = df['type'].astype(str).str.strip()
df['chunk_size'] = df['chunk_size'].astype(str).str.strip().replace({"nan": "None", "": "None"}).str.replace(r"\.0$", "", regex=True)

ranges_to_div = {
    "min_max": 1e8 - 2 + 1,
    "half_max": 1e8 - 1e8 // 2 + 1,
    "min_half": 1e8 // 2 - 2 + 1,
}

def calculate_speed(row: pd.Series) -> float:
    total_numbers = ranges_to_div.get(row['range_name'], 1e8 - 2 + 1)
    return (total_numbers * row['loops'] / row['time']) / 1e6

df['speed'] = df.apply(calculate_speed, axis=1)

df['std'] = df['std'] / df['time'] * df['speed']

chunk_order = ['None', '1', '10', '100', '1000', '5000']
types = ['static', 'dynamic', 'guided']
colors = {'static': '#1f77b4', 'dynamic': '#ff7f0e', 'guided': '#2ca02c'}

block_sizes = sorted(df['block_size'].unique())

fig, axes = plt.subplots(2, 3, figsize=(18, 10), dpi=150)
axes = axes.flatten()

for idx, block_size in enumerate(block_sizes):
    ax = axes[idx]
    block_df = df[df['block_size'] == block_size]
    
    x = np.arange(len(chunk_order))
    bar_width = 0.25

    for i, t in enumerate(types):
        sub_df = block_df[block_df['type'] == t].set_index('chunk_size').reindex(chunk_order).reset_index()
        
        pos = x + (i - 1) * bar_width
        
        bars = ax.bar(
            pos, sub_df['speed'], bar_width, 
            yerr=sub_df['std'], label=t, color=colors[t],
            capsize=4, edgecolor='black', linewidth=0.5, error_kw={'elinewidth': 1.2}
        )
        
        ax.bar_label(
            bars, fmt='%.1f', padding=4, 
            fontsize=7, weight='bold', color=colors[t], rotation=90
        )

    max_speed = block_df['speed'].max()
    ax.set_ylim(0, max_speed * 1.25)
    ax.set_xticks(x)
    ax.set_xticklabels(chunk_order, fontsize=9)

    ax.set_title(f'Wielkość bloku {block_size//1024} KB', fontsize=11, weight='bold')
    ax.set_ylabel('Prędkość przetwarzania [$10^6$ liczb/s]', fontsize=10)
    ax.set_xlabel('Tryb automatyczny / Wielkość chunku', fontsize=10)
    ax.tick_params(axis='x', labelrotation=0)

    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(fontsize=9, loc='upper right')

fig.suptitle('Kod K5 - porównanie prędkości przetwarzania w funkcji wielkości bloku oraz charakterystycznych rodzajów podziału pracy', fontsize=14, weight='bold', y=0.995)
plt.tight_layout()
plt.savefig("../outputs/K5.png")
