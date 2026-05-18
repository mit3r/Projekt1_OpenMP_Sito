import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Dane wejściowe (wklejone bezpośrednio jako tekst)
data = open("outputs/blocks_K3a_t20_min_max.csv", "r", encoding="utf-16").read()

# 2. Parsowanie danych do DataFrame (analogicznie do Twojego oryginalnego stylu)
rows = [line.split(';') for line in data.strip().split('\n')]
df = pd.DataFrame(rows, columns=['blockSize', 'time', 'std'])
df['blockSize'] = df['blockSize'].str.strip()
df['time'] = df['time'].astype(float)
df['std'] = df['std'].astype(float)

# 3. Konfiguracja struktury wykresu
fig, ax = plt.subplots(figsize=(12, 6), dpi=150)

# Pozycje na osi X i szerokość słupków
x = np.arange(len(df))
bar_width = 0.55  # Szerszy słupek, ponieważ nie dzielimy go na grupy
bar_color = '#1f77b4'  # Klasyczny, estetyczny niebieski kolor

# 4. Rysowanie słupków z błędami (bez pętli)
bars = ax.bar(
    x, df['time'], bar_width, 
    yerr=df['std'], color=bar_color,
    capsize=5, edgecolor='black', linewidth=0.5, error_kw={'elinewidth': 1.2}
)

# Automatyczne dodawanie wartości liczbowych nad słupkami
ax.bar_label(
    bars, fmt='%.3f', padding=6, 
    fontsize=9, weight='bold', color=bar_color
)

# 5. Ograniczenia, podpisy i estetyka
ax.set_ylim(0, 6.0)  # Dopasowanie zakresu do nowych danych (od 0 do 6 sekund)
ax.set_xticks(x)
# Dodana delikatna rotacja (15 stopni), aby długie nazwy blockSize nie nachodziły na siebie
ax.set_xticklabels(df['blockSize'], fontsize=10, rotation=15)

ax.set_title('Porównanie czasu wykonania w zależności od blockSize', fontsize=14, pad=20, weight='bold')
ax.set_xlabel('blockSize', fontsize=12, labelpad=10)
ax.set_ylabel('Czas wykonania [s]', fontsize=12)

ax.grid(True, axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True)  # Chowa linie siatki pod kolumnami

plt.tight_layout()
plt.show()