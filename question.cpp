#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>
using namespace std;

void rest(int a, int b, int c){
	int num1, num2, num3, num4;
	
	num1 = (a + b) % c;
	num2 = ((a % c) + (b % c)) % c;
	num3 = (a * b) % c;
	num4 = ((a % c) * (b % c)) % c;
	
	cout << num1 << '\n' << num2 << '\n' << num3 << '\n' << num4 << endl;
}

int gcd(int a, int b){
	int c;
	while (b != 0){
		c = a % b;
		a = b;
		b = c;
	}
	
	return a; // 최대공약수(유클리드 호제법)
}

int lcd(int a, int b){
	return (a * b) / gcd(a, b); // 최소공배수
}

void sumgcd(){
	int T;
	cin >> T;
	
	int number[T];
	
	for (int i = 0; i < T; i++){
		int K;
		cin >> K;
		
		for (int j = 0; j < K; j++){
			cin >> number[j];
		}
		
		int sum = 0;
		
		for (int a = 0; a < K; a++){
			for (int b = a + 1; b < K; b++){
				sum += gcd(number[a], number[b]);
			}
		}
		
		cout << sum << endl;
	}
// 주어진 수들의 최대공약수의 합
}

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

bool isPrimeNumber_2(int n){
	int root = sqrt(n);
	
	if (n == 2)
		return true;
	if (n == 1 || n % 2 ==  0)
		return false;
	
	for (int i = 3; i < root; i+=2){
		if (n % i == 0)
			return false;
	}
	
	return true;//->두번째 소수판별볍(n = a * b)
}

bool isPrimNumber_3(int n){
	static vector<int> primes {2, 3, 5, 7, 11, 13};
	
	int root = sqrt(n);
	
	if (n == 2)
		return true;
	if (n == 1 || n % 2 ==  0)
		return false;
	
	int a, b = 0;
	
	while (b <= root){
		b == primes[a++];
		if (n % b == 0)
			return false;
	}
	
	for (; b <= root; b+=2){
		if (n % b == 0)
			return false;
	}
	
	primes.push_back(n);
	
	return true;//-> 세번째 소수판별법(나중에 다시 공부)
}

/*int sum_prime(){
	int T; // T = 입력 개수
	cin >> T;
	
	int number[T];
	
	for (int i = 0; i < T; i++)
		cin >> number[i];
	
	int sum = 0;
	
	for (int i = 0; i < T; i++){
		if (isPrimeNumber_3(number[i]) == true)
			sum++;
	}
	
	return sum;//-> 총 소수 개수 구하기
}*/

int Goldbach(int number){
	static vector<int> primes {3, 5, 7, 11, 13};
	
	int a = primes[0];
	
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

int main(){
	int number;
	cin >> number;
	
	Goldbach(number);
	//cout << sum_prime() << endl;
	//sumgcd();
	
	/* int T;
	cin >> T;
	int K = T;
	
	int number[T];
	
	while (T != 0){
		int a, b;
		cin >> a >> b;
		
		number[T - 1] = lcd(a, b);
		T--;
	}
	
	for (int i = 0; i < K; i++){
		cout << number[K - 1 - i] << endl;
	} */
	
	
	return 0;
}
