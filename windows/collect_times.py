
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

for code in codes:
	print(f"Uruchamiam {code}...")

	path = os.path.join("./x64/Release/", code)

	for n, m in variants:

		print(f"{code}: {n} - {m}")
		name = f"./outputs/output_{code}_{n}_{m}.txt"

		if os.path.exists(name):
			print(f"Plik {name} już istnieje, pomijam...")
			continue

		output = open(name, "w")
		subprocess.run([path, f"-n {n}", f"-m {m}"], check=True, stdout=output, stderr=output)
		output.close()