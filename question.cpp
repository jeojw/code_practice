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
	// -> 소수 추가가 안됌....
	
	if (number - a > primes.back()){
		for (int i = a + 1; i < number; i++){
			if (isPrimeNumber(i) == true){
				primes.push_back(i);
				sort(primes.begin(), primes.end());
				primes.erase(unique(primes.begin(), primes.end()),primes.end()); // 중복 제거하는 알고리즘?
			}
		}
	} //소수 추가 알고리즘!
	
	/*for (int i = 0; i < primes.size(); i++){
		cout << primes[i] << '\t';
	}*/ // 단순 벡터 출력용 알고리즘
	
	int q = 0;
	
	while (a < number / 2){
		for (int j = 0; j < primes.size(); j++){
			if (number - a == primes[j]){
				cout << number << " = " << a << " + " << number - a << endl;
				return 0;
			}
			else
				continue;//continue를 통해서 number - a를 벡터내의 소수와 계속 비교함
		}
		q++;//만일 그래도 없을 경우 a값을 a가 number의 절반이 될때까지 반복문을 돌림 그 이유는 a < number - a
		a = primes[q++];
	}
	
	if (a == number / 2){
		if (isPrimeNumber(a) == true){
			cout << number << " = " << a << " + " << number - a << endl;
			return 0;
		}
		else{
			cout << "Goldbach's conjecture is wrong." << endl;
			return 0;
		}
	}
	else{
		cout << "Goldbach's conjecture is wrong." << endl;
		return 0;
	}
	return 0;
}
