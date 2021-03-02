#include "MinHeap.h"
#include <iostream>
#define MAX 100
using namespace std;

template <typename T>
MinHeap<T>::MinHeap(){
	ary = new T[MAX];
	size = 0;
}

template <typename T>
MinHeap<T>::~MinHeap(){
	delete[] ary;
}

template <typename T>
bool MinHeap<T>::IsEmpty() const{
	if (size == 0)
		return true;
	else
		return false;
}

template <typename T>
int MinHeap<T>::GetSize() const{
	return size;
}

template <typename T>
int MinHeap<T>::Insert(const T& data){
	if (size == 0){
		ary[1] = data;
		size++;
	}
	
	else{
		ary[size + 1] = data;
		size++;
		
		int me = size;
		while (me / 2 != 0){
			if (ary[me / 2] >= data)
				Swap(&ary[me / 2], &ary[me]);
		
			me /= 2;
		}
	}
	
	return 1;
}

template <typename T>
int MinHeap<T>::Delete(){
	ary[1] = ary[size];
	size--;
	
	int key = 1;
	while (key < size){
		if (ary[2] < ary[3]){
			if (ary[key] > ary[key * 2])
				Swap(&ary[key], &ary[key * 2]);

			key *= 2;
		}
		else{
			if (ary[key] > ary[key * 2 + 1])
				Swap(&ary[key], &ary[key * 2 + 1]);

			key = 2 * key + 1;
		}
	}
	
	return 1;
}

template <typename T>
void MinHeap<T>::Swap(T* a, T* b){
	T tmp = *a;
	*a = *b;
	*b = tmp;
}

template <typename T>
void MinHeap<T>::Print(){
	for (int i = 1; i < size + 1; i++)
		cout << ary[i] << " -> ";
}

/*int main(){
	MinHeap<int> heap;
	
	heap.Insert(4);
	heap.Insert(7);
	heap.Insert(3);
	heap.Insert(8);
	heap.Insert(5);
	heap.Insert(10);
	heap.Insert(6);
	heap.Delete();
	heap.Print();
	
	return 0;
}*/
