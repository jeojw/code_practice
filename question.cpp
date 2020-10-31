#include <iostream>
#include <vector>
using namespace std;

bool isPrimeNumber(int n){
	if (n == 2)
		return true;
	if (n == 1 || n % 2 ==  0)
		return false;
	
	for (int i = 3; i < n; i += 2){
		if (n % i == 0)
			return false;
	}
	
	return true;//->첫번째 소수판별법(n % 2)
}

int Goldbach(int number){
	static vector<int> primes {3, 5, 7, 11, 13};
	
	int a = primes[0];
	//int half = number / 2;
	int rest = number - a;
	// -> 소수 추가가 안됌....
	
	for (int j = 0; j < primes.size(); j++){
		if (rest > primes[j]){
			for (int k = a + 1; k <= rest; k++){ //-> 기존 수에서 13을 뺄 경우 13보다 큰 경우하고 작은 경우도 고려를 해봐야 할 거 같음
				if (isPrimeNumber(k) == true){
					primes.push_back(k);
					break;
				}
			}
			if (isPrimeNumber(rest) == true){
				primes.push_back(rest);
				break;
			}
		}
	}
	
	int q, w = 0;
	
	while (w <= primes.back()){
		if (primes[q] != primes.back()){
			w = primes[q++];
		}
	
		if (rest + a != number){
			cout << "Goldbach's conjecture is wrong" << endl;
			return 0;
		}
		else{
			cout << number << " = " << a << " + " << number - a << endl;
			return 0;
		}
	}
	
	return 0;
}
