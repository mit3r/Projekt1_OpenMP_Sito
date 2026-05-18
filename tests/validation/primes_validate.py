
import os
import subprocess
import hashlib
from colorama import Fore, Style

codes_dir = "../x64/Release/"
output_dir = "./primes_output/"
primes_file = "../tests/generated_primes/primes2^30.txt"

os.makedirs(output_dir, exist_ok=True)

outputs = filter(lambda x: x.endswith("_primes.txt"), os.listdir(output_dir))

for output in outputs:
    print(f"Sprawdzam {output}...")

    primes_f = open(primes_file, "r")

    count = 0

    for line in open(os.path.join(output_dir, output)):
        number = int(line.strip())
        prime = int(primes_f.readline().strip())

        if number != prime:
            print(f"Nieprawidłowa liczba: {Fore.RED}{number}{Style.RESET_ALL} w pliku {Fore.RED}{output}{Style.RESET_ALL}")
            break

        count += 1
    else:
        print(f"Sprawdzono {count} liczb. Plik {Fore.GREEN}{output}{Style.RESET_ALL} jest {Fore.GREEN}poprawny{Style.RESET_ALL}.")

    primes_f.close()
