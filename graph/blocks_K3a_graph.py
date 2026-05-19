import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO

# 1. Dane wejściowe
data = open("outputs_2/blocks_K3a_t20.csv", "r", encoding="utf-16").read()
times = 20

# 2. Parsowanie danych do DataFrame
df = pd.read_csv(
    StringIO(data),
    sep=';',
    header=None,
    names=['block_size_bytes', 'data_range', 'time', 'std'],
    skipinitialspace=True,
)

df['block_size_bytes'] = df['block_size_bytes'].astype(int)
df['data_range'] = df['data_range'].str.strip()
df['time'] = pd.to_numeric(df['time'].astype(str).str.replace(',', '.', regex=False))
df['std'] = pd.to_numeric(df['std'].astype(str).str.replace(',', '.', regex=False))
df['block_size_kb'] = df['block_size_bytes'] / 1024

# 3. Obliczanie liczby przetworzonych liczb na sekundę
ranges_to_div = {
    "min_max": 10e8 - 2 + 1,
    "half_max": 10e8 - 10e8 // 2 + 1,
    "min_half": 10e8 // 2 - 2 + 1,
}

# W milionach liczb na sekundę
def calculate_speed(row: pd.Series) -> float:
    total_numbers = ranges_to_div.get(row['data_range'], None)
    return (total_numbers / row['time']) / 1e6

df['speed'] = df.apply(calculate_speed, axis=1)

df['std'] = df['std'] / df['time'] * df['speed']

# 3. Konfiguracja struktury wykresu
block_order = sorted(df['block_size_kb'].unique())
range_order = df['data_range'].drop_duplicates().tolist()
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

# Pozycje na osi X i szerokość słupków
x = np.arange(len(block_order))
bar_width = 0.22

# 4. Rysowanie słupków z błędami
for i, data_range in enumerate(range_order):
    sub_df = df[df['data_range'] == data_range].set_index('block_size_kb').reindex(block_order).reset_index()
    offset = (i - (len(range_order) - 1) / 2) * bar_width

    bars = ax.bar(
        x + offset,
        sub_df['speed'],
        bar_width,
        yerr=sub_df['std'],
        label=display_labels.get(data_range, data_range),
        color=colors.get(data_range, None),
        capsize=5,
        edgecolor='black',
        linewidth=0.5,
        error_kw={'elinewidth': 1.2},
    )

    # Automatyczne dodawanie wartości liczbowych nad słupkami
    ax.bar_label(
        bars,
        fmt='%.3f',
        padding=6,
        fontsize=9,
        weight='bold',
        color=colors.get(data_range, 'black'),
        rotation=90,
    )

# 5. Ograniczenia, podpisy i estetyka
ax.set_ylim(150, 450)  # Zakres prędkości z pewnym marginesem
ax.set_xticks(x)
ax.set_xticklabels([f'{size:g}' for size in block_order], fontsize=10)

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
plt.show()