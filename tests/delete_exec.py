import os

dirs = os.listdir('../')

filtered_dirs = [d for d in dirs if os.path.isdir(os.path.join('../', d)) and d.startswith('Projekt')]

for i, directory in enumerate(filtered_dirs):
    try:
        os.remove(f"../{directory}/a.out")
    except FileNotFoundError:
        print(f"Nie znaleziono pliku a.out w katalogu {directory}.")
        continue
    else:
        print(f"Usunięto a.out w katalogu {directory} ({i + 1}/{len(filtered_dirs)})")
        