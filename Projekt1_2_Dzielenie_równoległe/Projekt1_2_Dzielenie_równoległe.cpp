#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <omp.h>

int main(int argc, char **argv)
{
	// Ustalanie zakresu
	int m = 2, n = pow(2, 20);

	for (int i = 0; i < argc; i++)
	{
		if (!strcmp(argv[i], "-m") && i + 1 < argc)
			m = atoi(argv[i + 1]);
		if (!strcmp(argv[i], "-n") && i + 1 < argc)
			n = atoi(argv[i + 1]);
	}

	// Właściwy algorytm

	bool *result = new bool[n - m + 1];
	std::memset(result, true, (n - m + 1) * sizeof(bool));

	bool *result2 = new bool[n - m + 1];
	std::memset(result2, true, (n - m + 1) * sizeof(bool));

	bool *primeArray = new bool[(int)(sqrt(n) + 1)];
	std::memset(primeArray, true, (sqrt(n) + 1) * sizeof(bool));

	double startTime = omp_get_wtime();
	for (int i = 2; i * i <= n; i++)
	{
		for (int j = 2; j * j <= i; j++)
		{
			if (primeArray[j] == true && i % j == 0)
			{
				primeArray[i] = false;
				break;
			}
		}
	}
	double endTime = omp_get_wtime();
	std::cout << "Czas obliczania liczb pierwszych do sqrt(n): " << endTime - startTime << " sekund" << std::endl;

	startTime = omp_get_wtime();
	for (int i = m; i <= n; i++)
	{
		for (int j = 2; j * j <= i; j++)
		{
			if (primeArray[j] == true && i % j == 0)
			{
				result[i - m] = false;
				break;
			}
		}
	}

	endTime = omp_get_wtime();
	std::cout << "Czas obliczania sekwencyjnych liczb pierwszych w przedziale [m, n]: " << endTime - startTime << " sekund" << std::endl;

	startTime = omp_get_wtime();

#pragma omp parallel
	{
// ? Jaki podział pracy ?
#pragma omp for schedule(dynamic)
		for (int i = m; i <= n; i++)
		{
			for (int j = 2; j * j <= i; j++)
			{
				if (primeArray[j] == true && i % j == 0)
				{
					result2[i - m] = false;
					break;
				}
			}
		}
	}
	endTime = omp_get_wtime();
	std::cout << "Czas obliczania liczb pierwszych w przedziale [m, n]: " << endTime - startTime << " sekund" << std::endl;

	// Wypisywanie wyników do pliku, jeśli podano flagę -o
	bool doPrint = false;
	for (int i = 0; i < argc; i++)
		doPrint = !strcmp(argv[i], "-o");

	if (doPrint)
	{
		// sekwencyjnie
		std::fstream file("primes_1.txt", std::ios::out);

		for (int i = m; i <= n; i++)
			if (result[i - m])
				file << i << std::endl;

		file.close();
		// równolegle
		std::fstream file2("primes_2.txt", std::ios::out);
		for (int i = m; i <= n; i++)
			if (result2[i - m])
				file2 << i << std::endl;
		file2.close();
	}

	delete[] result;
	delete[] result2;
	delete[] primeArray;
	return 0;
}
