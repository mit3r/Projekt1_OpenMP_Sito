import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO

# Słownik mapujący nazwy zakresów na liczbę iteracji
ranges_to_int = {
    "min_max": 10e8 - 2 + 1,
    "half_max": 10e8 - 10e8 // 2 + 1,
    "min_half": 10e8 // 2 - 2 + 1,
}

# Przykładowe dane (kilka wariantów, każdy ma 3 zakresy)

data = open("outputs_3/speed_comp.csv", "r", encoding="utf-8").read()

# data = """variant;range_name;avg_time;std_dev;loops;trials
# Kod_V1;min_max;1.5;0.05;1;5
# Kod_V1;half_max;0.8;0.03;1;5
# Kod_V1;min_half;0.4;0.01;1;5
# Kod_V2;min_max;1.1;0.04;1;5
# Kod_V2;half_max;0.6;0.02;1;5
# Kod_V2;min_half;0.3;0.01;1;5
# Kod_V3;min_max;0.9;0.02;1;5
# Kod_V3;half_max;0.5;0.02;1;5
# Kod_V3;min_half;0.25;0.01;1;5
# """

# Wczytywanie danych
df = pd.read_csv(
    StringIO(data),
    sep=';',
    header=0,
    names=["variant", "schedule", "chunk_size", "block_size", "range_name", "avg_time", "std_dev", "loops", "trials"],
    skipinitialspace=True,
    keep_default_na=False,
)

# Konwersja typów
df["variant"] = df["variant"].astype(str).str.strip()
df["range_name"] = df["range_name"].astype(str).str.strip()
for col in ["avg_time", "std_dev", "loops", "trials"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Obliczanie prędkości i odchylenia standardowego prędkości
df["avg_speed"] = df.apply(lambda row: (ranges_to_int.get(row["range_name"], None) * row["loops"] / row["avg_time"]) / 1e6, axis=1)
df["std_speed"] = df.apply(lambda row: row["std_dev"] / row["avg_time"] * row["avg_speed"], axis=1)

# Definiujemy kolejność zakresów oraz przypisane im kolory
range_order = ['min_max', 'half_max', 'min_half']
colors = {'min_max': '#1f77b4', 'half_max': '#ff7f0e', 'min_half': '#2ca02c'}
# Mapowanie nazw zakresów na czytelne etykiety LaTeX
display_labels = {
    'min_max': r'$[2, MAX]$',
    'half_max': r'$[\frac{MAX}{2}, MAX]$',
    'min_half': r'$[2, \frac{MAX}{2}]$',
}

# Unikalne warianty kodu (będą stanowić główne grupy na osi X)
variant_order = sorted(df['variant'].unique())

# Przygotowanie wykresu
fig, ax = plt.subplots(figsize=(12, 6), dpi=150)

x = np.arange(len(variant_order))
bar_width = 0.25  # Szerokość pojedynczego słupka

# Iterujemy po zakresach, żeby narysować je obok siebie dla każdego wariantu
for i, r_name in enumerate(range_order):
    # Filtrujemy dane dla konkretnego zakresu i układamy je w kolejności wariantów
    sub_df = df[df['range_name'] == r_name].set_index('variant').reindex(variant_order).reset_index()
    
    # Obliczamy pozycję słupków (przesunięcie w lewo/prawo od środka grupy)
    pos = x + (i - 1) * bar_width
    
    # Rysowanie serii słupków dla danego zakresu
    bars = ax.bar(
        pos, sub_df['avg_speed'], bar_width, 
        yerr=sub_df['std_speed'],
        label=display_labels.get(r_name, r_name), color=colors[r_name],
        capsize=4, edgecolor='black', linewidth=0.5, error_kw={'elinewidth': 1.2}
    )

    # Dodanie wartości nad słupkami (obrócone o 45 stopni dla czytelności)
    ax.bar_label(
        bars, fmt='%.1f', padding=6, 
        fontsize=8.5, weight='bold', color=colors[r_name], rotation=45
    )

# Estetyka i konfiguracja osi
ax.set_yscale("log")
ax.set_ylim(0, max(df['avg_speed'] * 5))  # Zapas na etykiety tekstowe nad słupkami
ax.set_xticks(x)
ax.set_xticklabels(variant_order, fontsize=11, weight='bold')

ax.set_title('Porównanie prędkości przetwarzania wariantów kodu dla różnych zakresów danych', fontsize=14, pad=25, weight='bold')
ax.set_xlabel('Wariant kodu', fontsize=12, labelpad=10)
ax.set_ylabel('Prędkość przetwarzania [$10^6$ liczb/s]', fontsize=12)

ax.grid(True, axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True)

# Legenda opisująca zakresy danych
ax.legend(title='Zakres danych', fontsize=11, title_fontsize=11, loc='upper left')

plt.tight_layout()
plt.show()