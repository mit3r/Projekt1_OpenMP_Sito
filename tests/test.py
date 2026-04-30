import sys

n = sys.argv[1] if len(sys.argv) > 1 else "20"
k = sys.argv[2] if len(sys.argv) > 2 else "50"

with open(f"generated_primes/primes2^{n}.txt", "r") as file:
    primes = file.read().splitlines() [:int(k)]

with open("primes_3.txt", "r") as file:
    primes2 = file.read().splitlines() [:int(k)]


print(primes)
print(primes2)

if primes == primes2:
    print("\nThe lists are the same.")
else:
    print("\nThe lists are different.")