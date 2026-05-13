#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <algorithm>
#include <omp.h>

// Struktura wyrównana do linii cache (64 bajty)
struct alignas(64) CacheLine {
	bool values[64];
};

int main(int argc, char** argv) {

	// Ustalanie zakresu
	int m = 2, n = pow(2, 30);

	for(int i = 0; i < argc; i++) {
		if(!strcmp(argv[i], "-m") && i + 1 < argc)
			m = atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-n") && i + 1 < argc)
			n = pow(2, atoi(argv[i + 1]));
	}

	double startTime = omp_get_wtime();

	// Właściwy algorytm
	int limit = (int)std::sqrt(n);
	bool* basePrimes = new bool[limit + 1];
	std::memset(basePrimes, true, limit + 1);
	basePrimes[0] = basePrimes[1] = false;

	for(int i = 2; i * i <= limit; i++) {
		if(basePrimes[i]) {
			for(int j = i * i; j <= limit; j += i) {
				basePrimes[j] = false;
			}
		}
	}

	// Sito dla przedziału [m, n]
	int rangeSize = n - m + 1;
	bool* result = new bool[rangeSize];
	std::memset(result, true, rangeSize * sizeof(bool));

	// Rozmiar segmentu dopasowany do rozmiaru cache L1 - 48 KB
	const int SEGMENT_SIZE = 48 * 1024;

	for(int low = m; low <= n; low += SEGMENT_SIZE) {
		int high = std::min(low + SEGMENT_SIZE - 1, n);

		for(int i = 2; i <= limit; i++) {
			if(basePrimes[i] == false)
				continue;

			int firstMultiple = (low + i - 1) / i * i;

			if(firstMultiple == i) firstMultiple += i;
			if(firstMultiple < i * i) firstMultiple = i * i;

			for(int j = firstMultiple; j <= high; j += i) {
				result[j - m] = false;
			}
		}
	}

	double endTime = omp_get_wtime();

	// 3. Wyniki
	int totalPrimeCount = 0;
	for(int i = 0; i < rangeSize; i++) if(result[i]) totalPrimeCount++;

	bool doPrint = false;
	for(int i = 0; i < argc; i++) if(!strcmp(argv[i], "-o")) doPrint = true;

	if(doPrint) {
		std::ofstream file("primes_3.txt");
		for(int i = 0; i < rangeSize; i++) {
			if(result[i]) file << i + m << "\n";
		}
		file.close();
	}

	std::cout << "Czas obliczania: " << endTime - startTime << " s" << std::endl;
	std::cout << "Liczba liczb pierwszych: " << totalPrimeCount << std::endl;

	// Czyszczenie pamięci
	delete[] basePrimes;
	delete[] result;

	return 0;
}