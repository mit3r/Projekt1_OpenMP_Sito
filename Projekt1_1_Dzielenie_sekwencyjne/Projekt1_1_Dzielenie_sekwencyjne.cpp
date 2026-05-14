// dzielenie sekwencyjne [k1]

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

	bool* basePrimes = new bool[(int)(sqrt(n) + 1)];
	std::memset(basePrimes, true, (sqrt(n) + 1) * sizeof(bool));
	basePrimes[0] = basePrimes[1] = false;

	bool* result = new bool[n - m + 1];
	std::memset(result, true, (n - m + 1) * sizeof(bool));

	double startWallTime = clock();
	double startProcTime = omp_get_wtime();

	for(int i = 2; i * i <= n; i++) {
		for(int j = 2; j * j <= i; j++) {
			if(basePrimes[j] == true && i % j == 0) {
				basePrimes[i] = false;
				break;
			}
		}
	}

	for(int i = m; i <= n; i++) {
		for(int j = 2; j * j <= i; j++) {
			if(basePrimes[j] == true && i % j == 0) {
				result[i - m] = false;
				break;
			}
		}
	}

	double endWallTime = clock();
	double endProcTime = omp_get_wtime();

	std::cout << "Wall_clock_time: " << (endWallTime - startWallTime) / CLOCKS_PER_SEC << std::endl;
	std::cout << "Processor_time: " << (endProcTime - startProcTime) << std::endl;
	std::cout << "Primes_found: " << std::count(result, result + (n - m + 1), true) << std::endl;

	utils_save_primes(result, m, n);

	delete[] result;
	delete[] basePrimes;
	return 0;
}