// dzielenie sekwencyjne [k1]

#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <omp.h>
#include <algorithm>

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

	double endTime = omp_get_wtime();
	std::cout << "Czas obliczania sekwencyjnych liczb pierwszych w przedziale [m, n]: " << endTime - startTime << " sekund" << std::endl;

	// Wypisywanie wyników do pliku, jeśli podano flagę -o
	bool doPrint = false;
	for (int i = 0; i < argc; i++)
		doPrint = !strcmp(argv[i], "-o");

	if (doPrint)
	{
		std::fstream file("primes_1.txt", std::ios::out);

		for (int i = m; i <= n; i++)
		{
			if (result[i - m])
			{

				file << i << std::endl;
			}
		}
		std::cout << "dlugsc listy: " << std::count(result, result + (n - m + 1), true) << std::endl;
		file.close();
	}

	delete[] result;
	delete[] primeArray;
	return 0;
}
