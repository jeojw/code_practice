#include <iostream>
#include "Queue.h"
using namespace std;

template <typename T>
Queue<T>::Queue(){
	Front = NULL;
	Rear = NULL;
	size = 0;
}

template <typename T>
Queue<T>::~Queue(){}

template <typename T>
int Queue<T>::GetSize() const{
	return size;
}

template <typename T>
bool Queue<T>::IsEmpty() const{
	if (size == 0)
		return true;
	else
		return false;
}

template <typename T>
int Queue<T>::Enqueue(const T& data){
	Node<T>* newNode = new Node<T>;
	newNode->data = data;
	newNode->next = NULL;
	
	if (size == 0)
		Front = newNode;
	
	else
		Rear->next = newNode;
	
	Rear = newNode;
	size++;
	
	return 1;
}

template <typename T>
int Queue<T>::Dequeue(){
	if (size == 0){
		cout << "No Items!!" << endl;
		return -1;
	}
	
	Node<T>* newFront = Front->next;
	Node<T>* del = Front;
	
	Front = newFront;
	delete del;
	size--;
	
	return 1;
}

template <typename T>
int Queue<T>::Peek(){
	if (size == 0){
		cout << "No Items!!" << endl;
		return -1;
	}
	
	cout << Front->data << endl;
	return 1;
}

template <typename T>
void Queue<T>::Print(){
	Node<T>* cur = Front;
	
	while (cur != NULL){
		cout << cur->data << " -> ";
		cur = cur->next;
	}
}

/*int main(){
	Queue<int> queue;
	
	queue.Enqueue(3);
	queue.Enqueue(4);
	queue.Enqueue(5);
	queue.Enqueue(2);
	queue.Enqueue(7);
	queue.Enqueue(8);
	queue.Peek();
	
	return 0;
}*/
