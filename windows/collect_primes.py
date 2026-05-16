
import os
import subprocess
import hashlib

codes_dir = "../x64/Release/"
output_dir = "./primes_output/"

os.makedirs(output_dir, exist_ok=True)

codes = filter(lambda x: x.endswith(".exe"), os.listdir(codes_dir))

for code in codes:
    print(f"Uruchamiam {code}...")

    path = os.path.join(codes_dir, code)

    output = open(f"{output_dir}{code}_primes.txt", "w")
    subprocess.run([path, "-o", f"-n {2}", f"-m {10e8}"], check=True, stdout=output)
    output.close()
