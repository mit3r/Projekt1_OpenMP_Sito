from sympy import isprime

if __name__ == "__main__":
    prime = []  
    k = 20
    n = 2**k
   
    for i in range(2, n+1):
        if isprime(i):
            prime.append(i)
            print(i/n)

    with open(f"generated_primes/primes2^{k}.txt", "w") as file:
        for x in prime:
            file.write(f"{x}\n")