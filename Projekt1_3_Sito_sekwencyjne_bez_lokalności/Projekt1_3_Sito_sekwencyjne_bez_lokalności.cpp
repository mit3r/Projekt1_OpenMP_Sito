#include <iostream>
#include <cstdlib>
#include <fstream>

int main(int argc, char** argv) {
	// Ustalanie zakresu
	int m = 2, n = pow(2, 20);

	for(int i = 0; i < argc; i++) {
		if(!strcmp(argv[i], "-m") && i + 1 < argc) 
			m = atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-n") && i + 1 < argc) 
			n = atoi(argv[i + 1]);
	}

	// Właściwy algorytm

	bool* result = new bool[n - m + 1];
	std::memset(result, true, (n - m + 1) * sizeof(bool));

	bool* primeArray = new bool[(int)(sqrt(n) + 1)];
	std::memset(primeArray, true, (sqrt(n) + 1) * sizeof(bool));

	for(int i = 2; i * i * i * i <= n; i++) {
		if(primeArray[i] == false) 
			continue;

		for(int j = i * i; j * j <= n; j++) 
			primeArray[j] = false;
	}

	for(int i = 2; i * i <= n; i++) {
		if(!primeArray[i]) continue;

		int firstMultiple = (m / i);

		if(firstMultiple <= 1)
			firstMultiple = 2 * i;
		else {
			firstMultiple = firstMultiple * i;
			if(m % i) firstMultiple += i;
		}

		for(int j = firstMultiple; j <= n; j += i) 
			result[j - m] = false;
	}

	// Wypisywanie wyników do pliku, jeśli podano flagę -o
	bool doPrint = false;
	for(int i = 0; i < argc; i++) doPrint = !strcmp(argv[i], "-o");

	if(doPrint) {
		std::fstream file("primes_3.txt", std::ios::out);

		for(int i = m; i <= n; i++)
			if(result[i - m]) file << i << std::endl;

		file.close();
	}

	return 0;
}
