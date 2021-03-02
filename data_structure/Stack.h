#ifndef ADDER_H 
#define ADDER_H
#include <iostream>
using namespace std;

template <typename T>
struct Node{
	T data;
	Node<T>* next;
};

template <typename T>
class Stack{
private:
	Node<T>* First;
	int size;
	
public:
	Stack();
	~Stack();
	
	bool IsEmpty() const;
	int GetSize() const;
	int Push(const T& data);
	int Pop();
	int Peek();
	Node<T>* Search(int Index);
	void Print();
};

#endif
