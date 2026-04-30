#include <iostream>
#include <cstdlib>
#include <fstream>


/*

Mieli conajmniej 30 minut, więc broń się panie Boże przed pustymi przebiegami.

*/

int main(int argc, char **argv)
{
	// Ustalanie zakresu
	int m = 2, n = pow(2, 30);

	for(int i = 0; i < argc; i++) {
		if(!strcmp(argv[i], "-m") && i + 1 < argc)
			m = atoi(argv[i + 1]);
		if(!strcmp(argv[i], "-n") && i + 1 < argc)
			n = atoi(argv[i + 1]);
	}

	// Właściwy algorytm

	bool *result = new bool[n - m + 1];
	std::memset(result, true, n - m + 1);

	bool* primeArray = new bool[(int)(sqrt(n) + 1)];
	std::memset(primeArray, true, (sqrt(n) + 1) * sizeof(bool));

    for(int i = 2; i * i <= n; i++) {
        for(int j = 2; j * j <= i; j++) {
            if(primeArray[j] == true && i % j == 0) {
				primeArray[i] = false; 
				break; 
			}
        }
    }

	int step = 0.05 * (n - m + 1), counter = 0;

    for(int i = m; i <= n; i++) {
        for(int j = 2; j * j <= i; j++) {
            if(primeArray[j] == true && i % j == 0) {
                result[i - m] = false; 
				break;
            }
        }

		if(++counter > step) {
			counter = 0;
			printf("Progress: %.2f%%\n", (float)(i - m + 1) / (n - m + 1) * 100);
		}
    }


	// Wypisywanie wyników do pliku, jeśli podano flagę -o
	bool doPrint = false;
	for(int i = 0; i < argc; i++) doPrint = !strcmp(argv[i], "-o");

	if(doPrint) {
		std::fstream file("primes_1.txt", std::ios::out);

		for(int i = m; i <= n; i++) 
			if(result[i - m]) file << i << std::endl;
	
		file.close();
	}

    return 0;
}
