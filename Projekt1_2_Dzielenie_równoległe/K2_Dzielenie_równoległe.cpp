// dzielenie równoległe [k2]

#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <omp.h>
#include <algorithm>
#include <time.h>

bool utils_doPrint = false;

void utils_get_args(int argc, char** argv, int* m, int* n, int* times, int* blockSize) {
	for(int i = 0; i < argc; i++) {
		if(!strcmp(argv[i], "-m") && i + 1 < argc)
			*m = std::atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-n") && i + 1 < argc)
			*n = std::atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-t") && i + 1 < argc)
			*times = std::atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-b") && i + 1 < argc)
			*blockSize = std::atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-o"))
			utils_doPrint = true;
	}
}

void utils_print_primes(bool* result, int m, int n) {
	if(!utils_doPrint) std::cout << std::count(result, result + (n - m + 1), true);
	else for(int i = m; i <= n; i++) if(result[i - m]) std::cout << i << std::endl;
}

int main(int argc, char** argv) {
	int m = 2, n = pow(10, 8);
	int times = 1, blockSize = 48 * 1024;

	utils_get_args(argc, argv, &m, &n, &times, &blockSize);

	int sqrt_n = (int)std::sqrt(n);
	int range = n - m + 1;

	bool* basePrimes = new bool[sqrt_n+1];
	bool* result = new bool[range];

	for(int k = 0; k < times; k++) {
		std::memset(basePrimes, true, (sqrt_n + 1) * sizeof(bool));
		std::memset(result, true, range * sizeof(bool));
		basePrimes[0] = basePrimes[1] = false;

		for(int i = 2; i <= sqrt_n; i++) {
			for(int j = 2; j <= (int)std::sqrt(i); j++) {
				if(basePrimes[j] == true && i % j == 0) {
					basePrimes[i] = false;
					break;
				}
			}
		}

		#pragma omp parallel for schedule(runtime)
		for(int i = m; i <= n; i++) {
			for(int j = 2; j <= (int)std::sqrt(i); j++) {
				if(basePrimes[j] == true && i % j == 0) {
					result[i - m] = false;
					break;
				}
			}
		}
	}

	utils_print_primes(result, m, n);

	delete[] result;
	delete[] basePrimes;

	return 0;
}