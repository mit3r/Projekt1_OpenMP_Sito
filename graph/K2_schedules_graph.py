import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import StringIO

ranges_to_int = {
    "min_max": 10e8 - 2 + 1,
    "half_max": 10e8 - 10e8 // 2 + 1,
    "min_half": 10e8 // 2 - 2 + 1,
}

data = open("outputs_3/K2_schedules.csv", "r", encoding="utf-8").read()

df = pd.read_csv(
    StringIO(data),
    sep=';',
    header=0,
    names=["variant", "schedule", "chunk_size", "block_size", "range_name", "avg_time", "std_dev", "loops", "trials"],
    skipinitialspace=True,
    keep_default_na=False,
)

df["schedule"] = df["schedule"].astype(str).str.strip()
df["chunk_size"] = (
    df["chunk_size"]
    .astype(str)
    .str.strip()
    .replace({"nan": "None", "": "None"})
    .str.replace(r"\.0$", "", regex=True)
)

for col in ["block_size", "avg_time", "std_dev", "loops", "trials"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["avg_speed"] = df.apply(lambda row: (ranges_to_int.get(row["range_name"], None) * row["loops"] / row["avg_time"]) / 1e6, axis=1)
df["std_speed"] = df.apply(lambda row: row["std_dev"] / row["avg_time"] * row["avg_speed"], axis=1)

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
    sub_df = df[df['schedule'] == t].set_index('chunk_size').reindex(chunk_order).reset_index()
    
    # Obliczanie przesunięcia dla każdego typu, aby stały obok siebie
    pos = x + (i - 1) * bar_width
    
    bars = ax.bar(
        pos, sub_df['avg_speed'], bar_width, 
        yerr=sub_df['std_speed'], label=t, color=colors[t],
        capsize=4, edgecolor='black', linewidth=0.5, error_kw={'elinewidth': 1.2}
    )
    
    # Automatyczne dodawanie wartości liczbowych nad słupkami
    ax.bar_label(
        bars, fmt='%.3f', padding=6, 
        fontsize=8.5, weight='bold', color=colors[t], rotation=45
    )

# 5. Ograniczenia, podpisy i estetyka
ax.set_ylim(0, max(df['avg_speed'] * 1.2)) # Ograniczenie osi Y na 20% powyżej maksymalnej prędkości
ax.set_xticks(x)
ax.set_xticklabels(chunk_order, fontsize=11)

ax.set_title('Kod K2 - porównanie prędkości przetwarzania dla różnych podziałów pracy', fontsize=14, pad=20, weight='bold')
ax.set_xlabel('Tryb automatyczny / Wielkość chunku ', fontsize=12, labelpad=10)
ax.set_ylabel('Prędkość przetwarzania [$10^6$ liczb/s]', fontsize=12)

ax.grid(True, axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True) # Chowa linie siatki pod kolumnami
ax.legend(title='Podział pracy (schedule)', fontsize=11, title_fontsize=11, loc='upper left')

plt.tight_layout()
plt.show()