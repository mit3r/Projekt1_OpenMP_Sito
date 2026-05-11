// sito równoległe bez lokalności odczyt/zapis [k4a]

#include <iostream>
#include <omp.h>
#include <cstdlib>
#include <math.h>
#include <climits>

int main()
{	
	const int n = INT_MAX; // 2^31-1 liczb
	//const int n = 100;
	
	long long limit2 = pow(n, 0.50);
	long long limit4 = pow(n, 0.25);

	bool* primeArray = new bool[n];
	for(int i = 2; i < n; i++) primeArray[i] = true;

	// Wstępne wykreślenie dla wielokrotności liczb mniejszych od pow(n, 1/4)
	for(long long i = 0; i < limit4; i++) {
		if(primeArray[i] == true) {
			for(long long j = i * i; j < n; j += i) { 
				primeArray[j] = false; 
			}
		}
	}
	
	#pragma omp parallel
	{
		#pragma omp for schedule(dynamic, 2)	
		for(long long i = 2; i < limit2; i++) {
			if(!primeArray[i]) continue;
			
			for(long long j = i * i; j < n; j += i) {
				if(primeArray[j]) primeArray[j] = false;
			}
		}
	}

	delete[] primeArray;

	return 0;
}
