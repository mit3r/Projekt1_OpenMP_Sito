// sito równoległe funkcyjne zapis [k4]

#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <omp.h>
#include <algorithm>
#include <time.h>

bool utils_doPrint = false;

void utils_get_args(int argc, char** argv, int* m, int* n) {
	for(int i = 0; i < argc; i++) {
		if(!strcmp(argv[i], "-m") && i + 1 < argc)
			*m = std::atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-n") && i + 1 < argc)
			*n = std::atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-o")) {
			utils_doPrint = true;
		}
	}
}

void utils_print_primes(bool* result, int m, int n) {
	if(!utils_doPrint) std::cout << std::count(result, result + (n - m + 1), true);
	else for(int i = m; i <= n; i++) if(result[i - m]) std::cout << i << std::endl;
}

int main(int argc, char** argv) {

	int m = 2, n = pow(10, 8);

	utils_get_args(argc, argv, &m, &n);

	int sqrt_n = (int)std::sqrt(n);

	bool* basePrimes = new bool[sqrt_n + 1];
	std::memset(basePrimes, true, sqrt_n + 1);
	basePrimes[0] = basePrimes[1] = false;
	
	int range = n - m + 1;

	bool* result = new bool[range];
	std::memset(result, true, range * sizeof(bool));

	for(int i = 2; i <= pow(n, 1 / 4); i++) {
		if(basePrimes[i] == true) {
			for(int j = i * i; j <= sqrt_n; j += i) { 
				basePrimes[j] = false;
			}
		}
	}

	const int blockSize = 12 * 1024;
	
	#pragma omp parallel for schedule(dynamic)
	for(int low = m; low <= n; low += blockSize) {
		int high = std::min(low + blockSize - 1, n);

		for(int i = 2; i <= sqrt_n; i++) {
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

	utils_print_primes(result, m, n);

	delete[] result;
	delete[] basePrimes;

	return 0;
}