#include <iostream>
#define MAX 100
using namespace std;

template <typename T>
class MaxHeap{
private:
	T ary[MAX];
	T data;
	int size;
	
public:
	MaxHeap();
	~MaxHeap();
	
	bool IsEmpty() const;
	int GetSize() const;
	int Insert(const T& data);
	int Delete(const T& data);
	int Retreive(const T& data);
	void Print();
};

template <typename T>
MaxHeap<T>::MaxHeap(){
	size = 0;
}

template <typename T>
MaxHeap<T>::~MaxHeap(){}

template <typename T>
bool MaxHeap<T>::IsEmpty() const{
	if (size == 0)
		return true;
	else
		return false;
}

template <typename T>
int MaxHeap<T>::GetSize() const{
	return size;
}

template <typename T>
int MaxHeap<T>::Insert(const T& data){
	if (size == 0){
		ary[1] = data;
		size++;
	}
	
	else{
		ary[size + 1] = data;
		size++;
		
		int half = size / 2;
		while (half != 0){
			if (ary[half] <= data){
				if (size % 2 == 0){
					T tmp = ary[half];
					ary[half] = ary[half * 2];
					ary[half * 2] = tmp;
				}
				else{
					T tmp = ary[half];
					ary[half] = ary[half * 2 + 1];
					ary[half * 2 + 1] = tmp;
				}
			}
			half /= 2;
		}
	}
	
	return 1;
}

template <typename T>
void MaxHeap<T>::Print(){
	for (int i = 1; i < size + 1; i++)
		cout << ary[i] << " -> ";
}

int main(){
	MaxHeap<int> heap;
	
	heap.Insert(4);
	heap.Insert(7);
	heap.Insert(3);
	heap.Insert(8);
	heap.Insert(5);
	heap.Print();
	
	return 0;
}
