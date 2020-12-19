#ifndef ADDER_H 
#define ADDER_H

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

////////////////////////////////////////////

#include <iostream>
#include "Stack.h"
using namespace std;

template <typename T>
Stack<T>::Stack(){
	First = NULL;
	size = 0;
}

template <typename T>
Stack<T>::~Stack(){}

template <typename T>
bool Stack<T>::IsEmpty() const{
	if (size == 0)
		return true;
	else
		return false;
}

template <typename T>
int Stack<T>::GetSize() const{
	return size;
}

template <typename T>
int Stack<T>::Push(const T& data){
	Node<T>* newNode = new Node<T>;
	newNode->data = data;
	newNode->next = NULL;
	
	if (size == 0)
		First = newNode;
	
	else{
		Node<T>* cur = First;
		while (cur->next != NULL)
			cur = cur->next;
		
		cur->next = newNode;
	}
	
	size++;
	
	return 1;
}

template <typename T>
int Stack<T>::Pop(){
	if (size == 0){
		cout << "Stack is Empty!!" << endl;
		return -1;
	}
	
	Node<T>* prev = Search(size - 1);
	Node<T>* del = prev->next;
	
	prev->next = NULL;
	delete del;
	
	size--;
	
	return 1;
}

template <typename T>
int Stack<T>::Peek(){
	Node<T>* cur = First;
	
	while (cur->next != NULL)
		cur = cur->next;

	cout << cur->data << " -> ";
	
	return 1;
}

template <typename T>
Node<T>* Stack<T>::Search(int Index){
	Node<T>* cur = First;
	for (int i = 0; i < Index - 1; i++)
		cur = cur->next;
	
	return cur;
}

template <typename T>
void Stack<T>::Print(){
	Node<T>* cur = First;
	
	while (cur!= NULL){
		cout << cur->data << " -> ";
		cur = cur->next;
	}
		
}
