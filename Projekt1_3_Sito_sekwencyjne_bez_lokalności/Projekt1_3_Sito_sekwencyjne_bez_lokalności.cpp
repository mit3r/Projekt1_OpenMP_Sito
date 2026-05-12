// sito sekwencyjne bez lokalności "funkcyjne" [k3]

#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <cstring>
#include <algorithm>
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
			n = pow(2, atoi(argv[i + 1]));
	}

	// Właściwy algorytm
	int limit = sqrt(n);
	bool *primeArray = new bool[limit + 1];
	std::memset(primeArray, true, (limit + 1) * sizeof(bool));
	primeArray[0] = primeArray[1] = false;

	for (int i = 2; i * i <= limit; i++)
	{
		if (primeArray[i])
		{
			for (int j = i * i; j <= limit; j += i)
			{
				primeArray[j] = false;
			}
		}
	}

	// Sito dla przedziału [m, n]
	int rangeSize = n - m + 1;
	bool *result = new bool[rangeSize];
	std::memset(result, true, rangeSize * sizeof(bool));

	double startTime = omp_get_wtime();
	for (int i = 2; i <= limit; i++)
	{
		if (!primeArray[i])
			continue;

		int firstMultiple = (m / i) * i;
		if (firstMultiple < m)
			firstMultiple += i;

		if (firstMultiple <= i)
			firstMultiple = i * 2;

		for (int j = firstMultiple; j <= n; j += i)
		{
			result[j - m] = false;
		}
	}
	double endTime = omp_get_wtime();
	std::cout << "Czas obliczania liczb pierwszych w przedziale [m, n]: " << endTime - startTime << " sekund" << std::endl;

	// Wypisywanie wyników do pliku, jeśli podano flagę -o
	bool doPrint = false;
	for (int i = 0; i < argc; i++)
	{
		if (!strcmp(argv[i], "-o"))
			doPrint = true;
	}

	if (doPrint)
	{
		std::fstream file("primes_3.txt", std::ios::out);
		for (int i = m; i <= n; i++)
		{
			if (result[i - m])
				file << i << '\n';
		}
		std::cout << "dlugsc listy: " << std::count(result, result + rangeSize, true) << std::endl;
		file.close();
	}

	delete[] primeArray;
	delete[] result;

	return 0;
}