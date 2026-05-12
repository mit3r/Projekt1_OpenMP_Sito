// sito sekwencyjne z lokalnością "domenowe" [k3a]
#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <algorithm>
#include <omp.h>

//64 KB pamięci
constexpr int SEGMENT_SIZE = 65536;

int main(int argc, char **argv)
{
    // Ustalanie zakresu
    int m = 2;
    int n = pow(2, 20);

    for (int i = 0; i < argc; i++)
    {
        if (!strcmp(argv[i], "-m") && i + 1 < argc)
            m = std::atoi(argv[i + 1]);
        if (!strcmp(argv[i], "-n") && i + 1 < argc)
            n = pow(2, std::atoi(argv[i + 1]));
    }

    double startTime = omp_get_wtime();
    int limit = std::sqrt(n);
    bool *basePrimes = new bool[limit + 1];
    std::memset(basePrimes, true, (limit + 1) * sizeof(bool));
    basePrimes[0] = basePrimes[1] = false;

    for (int i = 2; i * i <= limit; i++)
    {
        if (basePrimes[i])
        {
            for (int j = i * i; j <= limit; j += i)
            {
                basePrimes[j] = false;
            }
        }
    }

    int *primes = new int[limit];
    int primeCount = 0;
    for (int i = 2; i <= limit; i++)
    {
        if (basePrimes[i])
        {
            primes[primeCount++] = i;
        }
    }

    bool *segment = new bool[SEGMENT_SIZE];

    int totalPrimeCount = 0;
    bool doPrint = false;
    for (int i = 0; i < argc; i++)
    {
        if (!strcmp(argv[i], "-o"))
        {
            doPrint = true;
            break;
        }
    }

    std::fstream file;
    if (doPrint)
        file.open("primes.txt", std::ios::out);

    for (int low = m; low <= n; low += SEGMENT_SIZE)
    {
        int high = std::min(low + SEGMENT_SIZE - 1, n);
        int currentSegmentSize = high - low + 1;

        std::memset(segment, true, currentSegmentSize * sizeof(bool));

        for (int p = 0; p < primeCount; p++)
        {
            int i = primes[p];

            int firstMultiple = (low / i);
            if (firstMultiple <= 1)
            {
                firstMultiple = i + i;
            }
            else if (low % i != 0)
            {
                firstMultiple = (firstMultiple * i) + i;
            }
            else
            {
                firstMultiple = (firstMultiple * i);
            }

            for (int j = firstMultiple; j <= high; j += i)
            {
                segment[j - low] = false;
            }
        }

        for (int i = 0; i < currentSegmentSize; i++)
        {
            if (segment[i])
            {
                totalPrimeCount++;
                if (doPrint)
                    file << (low + i) << "\n";
            }
        }
    }

    if (doPrint)
    {
        file.close();
    }

    // w tym przypadku wliczamy też czas dorzucenia do pliku i zliczenia
    // trzebaby chyba ujednolicic wypisywanie wynikow wszędzie (określić jak definiujemy czas )
    double endTime = omp_get_wtime();
    std::cout << "Czas obliczania: " << endTime - startTime << " sekund" << std::endl;
    std::cout << "dlugosc listy: " << totalPrimeCount << std::endl;

    delete[] basePrimes;
    delete[] primes;
    delete[] segment;

    return 0;
}