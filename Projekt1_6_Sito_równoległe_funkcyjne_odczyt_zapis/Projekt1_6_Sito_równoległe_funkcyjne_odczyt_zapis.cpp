// sito równoległe funkcyjne odczyt-zapis [k4a]

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

    int limit = (int)std::sqrt(n);

    bool* basePrimes = new bool[limit + 1];
    std::memset(basePrimes, true, limit + 1);
    basePrimes[0] = basePrimes[1] = false;

	int range = n - m + 1;

    bool* result = new bool[range];
    std::memset(result, true, range * sizeof(bool));

    double startWallTime = omp_get_wtime();
    double startProcTime = clock();

    for(int i = 2; i <= limit; i++) {
        for(int j = 2; j * j <= i; j++) {
            if(basePrimes[j] == true && i % j == 0) {
                basePrimes[i] = false;
                break;
            }
        }
    }

#pragma omp parallel for schedule(static)
    for(int i = m; i <= n; i++) 
    {
        for(int j = 2; j * j <= i; j++) 
        {
            if(basePrimes[j] == true && i % j == 0) 
            {
                if(result[i-m]) result[i - m] = false;
                break;
            }
        }
    }

    double endWallTime = omp_get_wtime();
    double endProcTime = clock();

    std::cout << "Wall_clock_time: " << (endWallTime - startWallTime) << std::endl;
    std::cout << "Processor_time: " << (endProcTime - startProcTime) / CLOCKS_PER_SEC << std::endl;
    std::cout << "Primes_found: " << std::count(result, result + (n - m + 1), true) << std::endl;

    utils_save_primes(result, m, n);

    delete[] result;
    delete[] basePrimes;

    return 0;
}