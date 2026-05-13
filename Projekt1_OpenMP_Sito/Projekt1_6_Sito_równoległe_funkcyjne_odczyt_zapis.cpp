// sito równoległe funkcyjne zapis [k4]
#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <omp.h>
#include <algorithm>

int main(int argc, char** argv) {
    // Ustalanie domyślnego zakresu (n = 2^20)
    int m = 2;
    int n = pow(2, 20);

    // Parsowanie argumentów z konsoli
    for(int i = 0; i < argc; i++) {
        if(!strcmp(argv[i], "-m") && i + 1 < argc)
            m = std::atoi(argv[i + 1]);
        if(!strcmp(argv[i], "-n") && i + 1 < argc)
            n = pow(2, std::atoi(argv[i + 1]));
    }

    bool* result = new bool[n - m + 1];
    std::memset(result, true, (n - m + 1) * sizeof(bool));

    bool* basePrimes = new bool[(int)(sqrt(n) + 1)];
    std::memset(basePrimes, true, (sqrt(n) + 1) * sizeof(bool));

    // Inicjalizacja tablicy dla sqrt(n)
    int limit = std::sqrt(n);
    basePrimes[0] = basePrimes[1] = false;

    double startTime = omp_get_wtime();

    // Wyznaczanie bazowych liczb pierwszych do sqrt(n) (sekwencyjnie)
    for(int i = 2; i <= limit; i++) {
        for(int j = 2; j * j <= i; j++) {
            if(basePrimes[j] == true && i % j == 0) {
                basePrimes[i] = false;
                break;
            }
        }
    }

#pragma omp parallel for schedule(dynamic)
    for(int i = m; i <= n; i++) {
        for(int j = 2; j * j <= i; j++) {
            if(basePrimes[j] == true && i % j == 0) {
                result[i - m] = false;
                break;
            }
        }
    }

    double endTime = omp_get_wtime();
    std::cout << "Czas obliczania liczb pierwszych w przedziale [m, n]: " << endTime - startTime << " sekund" << std::endl;

    // Wypisywanie wyników do pliku, jeśli podano flagę -o
    bool doPrint = false;
    for(int i = 0; i < argc; i++) {
        if(!strcmp(argv[i], "-o")) {
            doPrint = true;
            break;
        }
    }

    if(doPrint) {
        std::fstream file("primes_2.txt", std::ios::out);

        for(int i = m; i <= n; i++) {
            if(result[i - m]) {
                file << i << "\n";
            }
        }

        file.close();

        std::cout << "dlugosc listy: " << std::count(result, result + (n - m + 1), true) << std::endl;
    }

    delete[] result;
    delete[] basePrimes;
    return 0;
}