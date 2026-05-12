import subprocess
import glob
import os

dirs = os.listdir('../')

filtered_dirs = [d for d in dirs if os.path.isdir(os.path.join('../', d)) and d.startswith('Projekt')]

for i, dir in enumerate(filtered_dirs):
    polecenie = [f"../{dir}/a.out", "-n", "25"]
    try:
        result = subprocess.run(polecenie, capture_output=True, text=True, check=True)
        print(f"Wyjście programu: {dir}:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Błąd kompilacji w katalogu {dir}:\n", e.stderr)
    except FileNotFoundError:
        print(f"Nie znaleziono pliku a.out w katalogu {dir}. Upewnij się, że program został skompilowany.\n")
        continue
    