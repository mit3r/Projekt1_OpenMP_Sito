import subprocess
import glob
import os

dirs = os.listdir('../')

filtered_dirs = [d for d in dirs if os.path.isdir(os.path.join('../', d)) and d.startswith('Projekt')]

for i, dir in enumerate(filtered_dirs):
    source_file = glob.glob(f"../{dir}/*.cpp")
    compile_command = ["g++", "-fopenmp"] + source_file + ["-O3", "-o", f"../{dir}/a.out"]
    try:
        subprocess.run(compile_command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Błąd kompilacji w katalogu {dir}:\n", e.stderr)
    else:
        print(f"Skompilowano pomyślnie ({i + 1}/{len(filtered_dirs)})")
