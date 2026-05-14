
import os
import sys
import subprocess


codes = filter(lambda x: x.endswith(".exe"), os.listdir("./x64/Release/"))


for code in codes:
	print(f"Uruchamiam {code}...")

	path = os.path.join("./x64/Release/", code)
	subprocess.run([path, "-n 2", "-m 1000000"], check=True) 
	