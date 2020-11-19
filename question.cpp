#include <iostream>
using namespace std;

int sum_split(int number){
	int data[50];
	
	if (number == 1)
		return 1;
	if (number == 2)
		return 2;
	if (number == 3)
		return 4;
	
	if (data[number] != 0)
		return data[number];
	
	else
		return data[number] = sum_split(number - 1) + sum_split(number - 2) + sum_split(number - 3);
}	

int main(){
	int number;
	cin >> number;
	cout << sum_split(number) << endl;
	
	return 0;
}
