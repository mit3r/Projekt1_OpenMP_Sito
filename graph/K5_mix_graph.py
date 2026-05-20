import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Dane wejściowe
data = open("outputs_3/K5_mix.csv", "r", encoding="utf-8").read()

# 2. Parsowanie danych do DataFrame
from io import StringIO
df = pd.read_csv(
    StringIO(data),
    sep=';',
    header=0,
    names=["name", "type", "chunk_size", "block_size", "range_name", "time", "std", "loops", "trials"],
    skipinitialspace=True,
)

# Czyszczenie danych (stripping i konwersja typów)
df['type'] = df['type'].astype(str).str.strip()
df['chunk_size'] = df['chunk_size'].astype(str).str.strip().replace({"nan": "None", "": "None"}).str.replace(r"\.0$", "", regex=True)

# 3. Obliczanie liczby przetworzonych liczb na sekundę
ranges_to_div = {
    "min_max": 10e8 - 2 + 1,
    "half_max": 10e8 - 10e8 // 2 + 1,
    "min_half": 10e8 // 2 - 2 + 1,
}

# W milionach liczb na sekundę
def calculate_speed(row: pd.Series) -> float:
    total_numbers = ranges_to_div.get(row['range_name'], 10e8 - 2 + 1)
    return (total_numbers * row['loops'] / row['time']) / 1e6

df['speed'] = df.apply(calculate_speed, axis=1)

df['std'] = df['std'] / df['time'] * df['speed']

# 3. Konfiguracja struktury grup i wykresu
chunk_order = ['None', '1', '10', '100', '1000', '5000']
types = ['static', 'dynamic', 'guided']
colors = {'static': '#1f77b4', 'dynamic': '#ff7f0e', 'guided': '#2ca02c'}

# 4. Pobierz unikalne block_size'y (posortowane)
block_sizes = sorted(df['block_size'].unique())

# 5. Twórz subploty dla każdego block_size'u
fig, axes = plt.subplots(2, 3, figsize=(18, 10), dpi=150)
axes = axes.flatten()

for idx, block_size in enumerate(block_sizes):
    ax = axes[idx]
    block_df = df[df['block_size'] == block_size]
    
    # Definiowanie szerokości słupków i pozycji na osi X
    x = np.arange(len(chunk_order))
    bar_width = 0.25

    # Rysowanie słupków z błędami
    for i, t in enumerate(types):
        sub_df = block_df[block_df['type'] == t].set_index('chunk_size').reindex(chunk_order).reset_index()
        
        # Obliczanie przesunięcia dla każdego typu, aby stały obok siebie
        pos = x + (i - 1) * bar_width
        
        bars = ax.bar(
            pos, sub_df['speed'], bar_width, 
            yerr=sub_df['std'], label=t, color=colors[t],
            capsize=4, edgecolor='black', linewidth=0.5, error_kw={'elinewidth': 1.2}
        )
        
        # Automatyczne dodawanie wartości liczbowych nad słupkami
        ax.bar_label(
            bars, fmt='%.1f', padding=4, 
            fontsize=7, weight='bold', color=colors[t], rotation=90
        )

    # Ograniczenia, podpisy i estetyka
    max_speed = block_df['speed'].max()
    ax.set_ylim(0, max_speed * 1.25)  # 15% marginesie na górze
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
plt.show()