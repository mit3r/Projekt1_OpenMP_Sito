import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Dane wejściowe
data = open("outputs_2/schedules_K4_t10_min_max_avg5.csv", "r", encoding="utf-16").read()
times = 10

# 2. Parsowanie danych do DataFrame
rows = [line.split(';') for line in data.strip().split('\n')]
df = pd.DataFrame(rows, columns=['type', 'chunk_size', 'time', 'std'])
df['type'] = df['type'].str.strip()
df['chunk_size'] = df['chunk_size'].str.strip()
df['time'] = df['time'].astype(float)
df['std'] = df['std'].astype(float)

# 3. Obliczanie liczby przetworzonych liczb na sekundę
ranges_to_div = {
    "min_max": 10e8 - 2 + 1,
    "half_max": 10e8 - 10e8 // 2 + 1,
    "min_half": 10e8 // 2 - 2 + 1,
}

# W milionach liczb na sekundę
def calculate_speed(row: pd.Series) -> float:
    total_numbers = ranges_to_div.get("min_max", None)
    return (total_numbers / row['time']) / 1e6

df['speed'] = df.apply(calculate_speed, axis=1)

df['std'] = df['std'] / df['time'] * df['speed']

# 3. Konfiguracja struktury grup i wykresu
chunk_order = ['None', '1', '10', '100', '1000', '5000']
types = ['static', 'dynamic', 'guided']
colors = {'static': '#1f77b4', 'dynamic': '#ff7f0e', 'guided': '#2ca02c'}

fig, ax = plt.subplots(figsize=(12, 6), dpi=150)

# Definiowanie szerokości słupków i pozycji na osi X
x = np.arange(len(chunk_order))
bar_width = 0.25

# 4. Rysowanie słupków z błędami
for i, t in enumerate(types):
    sub_df = df[df['type'] == t].set_index('chunk_size').reindex(chunk_order).reset_index()
    
    # Obliczanie przesunięcia dla każdego typu, aby stały obok siebie
    pos = x + (i - 1) * bar_width
    
    bars = ax.bar(
        pos, sub_df['speed'], bar_width, 
        yerr=sub_df['std'], label=t, color=colors[t],
        capsize=4, edgecolor='black', linewidth=0.5, error_kw={'elinewidth': 1.2}
    )
    
    # Automatyczne dodawanie wartości liczbowych nad słupkami
    ax.bar_label(
        bars, fmt='%.3f', padding=6, 
        fontsize=8.5, weight='bold', color=colors[t], rotation=45
    )

# 5. Ograniczenia, podpisy i estetyka
ax.set_ylim(200, 1300) # Ograniczenie osi Y do 6 sekund
ax.set_xticks(x)
ax.set_xticklabels(chunk_order, fontsize=11)

ax.set_title('Kod K4 - porównanie prędkości przetwarzania dla różnych podziałów pracy', fontsize=14, pad=20, weight='bold')
ax.set_xlabel('Tryb automatyczny / Wielkość chunku ', fontsize=12, labelpad=10)
ax.set_ylabel('Prędkość przetwarzania [$10^6$ liczb/s]', fontsize=12)

ax.grid(True, axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True) # Chowa linie siatki pod kolumnami
ax.legend(title='Podział pracy (schedule)', fontsize=11, title_fontsize=11, loc='upper right')

plt.tight_layout()
plt.show()