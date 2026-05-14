// sito sekwencyjne z lokalnością [k3a]

#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <omp.h>
#include <algorithm>
#include <time.h>

bool utils_doPrint = false;

void utils_get_args(int argc, char** argv, int& m, int& n) {
	for(int i = 0; i < argc; i++) {
		if(!strcmp(argv[i], "-m") && i + 1 < argc)
			m = std::atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-n") && i + 1 < argc)
			n = std::atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-o")) {
			utils_doPrint = true;
		}
	}
}

void utils_save_primes(bool* result, int m, int n) {
	if(!utils_doPrint) return;
	std::fstream file("primes.txt", std::ios::out);
	for(int i = m; i <= n; i++) {
		if(result[i - m]) {
			file << i << std::endl;
		}
	}
	file.close();
}

int main(int argc, char** argv) {

	int m = 2, n = pow(10, 8);

	utils_get_args(argc, argv, m, n);

	int limit = (int)std::sqrt(n);

	bool* basePrimes = new bool[limit + 1];
	std::memset(basePrimes, true, limit + 1);
	basePrimes[0] = basePrimes[1] = false;

	int range = n - m + 1;

	bool* result = new bool[range];
	std::memset(result, true, range * sizeof(bool));

	double startWallTime = omp_get_wtime();
	double startProcTime = clock();

	for(int i = 2; i * i <= limit; i++) {
		if(basePrimes[i]) {
			for(int j = i * i; j <= limit; j += i) {
				basePrimes[j] = false;
			}
		}
	}

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

	double endWallTime = omp_get_wtime();
	double endProcTime = clock();

	std::cout << "Wall_clock_time: " << (endWallTime - startWallTime) << std::endl;
	std::cout << "Processor_time: " << (endProcTime - startProcTime) / CLOCKS_PER_SEC << std::endl;
	std::cout << "Primes_found: " << std::count(result, result + range, true) << std::endl;

	utils_save_primes(result, m, n);

	delete[] basePrimes;
	delete[] result;

	return 0;
}