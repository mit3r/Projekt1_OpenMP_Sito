
import os
import subprocess

codes = filter(lambda x: x.endswith(".exe"), os.listdir("./x64/Release/"))

mini = 2
half = 10e8 // 2
maksi = 10e8

variants = [
  (mini, maksi), # pełny zakres
  (half, maksi), # górny zakres
  (mini, half), # dolny zakres
  ]

file = open("results.txt", "w")

for code in codes:
  print(f"Uruchamiam {code}...")

  path = os.path.join("./x64/Release/", code)

  for n, m in variants:

    print(f"{code}: {n} - {m}")
    file.write(f"{code}: {n} - {m}\n")

    
    subprocess.run([path, f"-n {n}", f"-m {m}"], check=True)
    
file.close()