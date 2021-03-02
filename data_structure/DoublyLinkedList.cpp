#include <iostream>
#include "DoublyLinkedList.h"
using namespace std;

template <typename T>
DoublyLinkedList<T>::DoublyLinkedList(){
	head = NULL;
	tail = NULL;
	length = 0;
}

template <typename T>
DoublyLinkedList<T>::~DoublyLinkedList(){}

template <typename T>
bool DoublyLinkedList<T>::IsEmpty() const{
	if (length == 0)
		return true;
	else
		return false;
}

template <typename T>
int DoublyLinkedList<T>::GetLength() const{
	return length;
}

template <typename T>
int DoublyLinkedList<T>::PushBack(const T& data){
	Node<T>* newNode = new Node<T>;
	newNode->data = data;
	
	if (length == 0)
		head = newNode;
	
	else{
		tail->next = newNode;
		newNode->prev = tail;
	}
	
	tail = newNode;
	
	length++;
	
	return 1;
}

template <typename T>
int DoublyLinkedList<T>::Insert(const T& data, int Index){
	Node<T>* Pre = Search(Index - 1);
	Node<T>* newNode = new Node<T>;
	newNode->data = data;
	
	if ((length <= 1) || (Index == length)){
		cout << "Use PushBack!!" << endl;
		return -1;
	}
	
	if (Index <= 0){
		cout << "Index Error!!" << endl;
		return -1;
	}
	
	if (Index == 1){
		newNode->next = head;
		head->prev = newNode;
		
		head = newNode;
		
		length++;
		
		return 1;
	}
	
	newNode->next = Pre->next;
	(Pre->next)->prev = newNode;
	Pre->next = newNode;
	newNode->prev = Pre;
	
	length++;
	
	return 1;
}

template <typename T>
Node<T>* DoublyLinkedList<T>::Search(int Index){
	Node<T>* cur;
	
	if (Index <= (length / 2)){
		cur = head;
		for (int i = 0; i < Index - 1; i++)
			cur = cur->next;
		
		return cur;
	}
	
	else{
		cur = tail;
		for (int j = 0; j < (length - Index) - 1; j++)
			cur = cur->prev;
		
		return cur;
	}
}

template <typename T>
int DoublyLinkedList<T>::Pop(){
	if (length == 0){
		cout << "List is Empty!!" << endl;
		return -1;
	}
	Node<T>* Pre = tail->prev;
	Node<T>* del = tail;
	
	Pre->next = NULL;
	delete del;
	
	length--;
	
	return 1;
}

template <typename T>
int DoublyLinkedList<T>::Delete(int Index){
	if (length == 0){
		cout << "List is Empty!!" << endl;
		return -1;
	}
	
	if ((Index <= 0) || (Index > length)){
		cout << "Over the range!!" << endl;
		return -1;
	}
	
	if (Index == length){
		cout << "Use Pop!!!" << endl;
		return -1;
	}
	
	if (Index == 1){
		Node<T>* Next = head->next;
		Node<T>* del = head;
		
		Next->prev = NULL;
		head = Next;
		
		delete del;
		
		length--;
		
		return 1;
	}
	
	Node<T>* Pre = Search(Index - 1);
	Node<T>* del = Pre->next;
	
	Pre->next = del->next;
	(del->next)->prev = Pre;
	
	delete del;
	
	length--;
	
	return 1;
}

template <typename T>
void DoublyLinkedList<T>::Print(){
	if (length == 0)
		cout << "No Items!!" << endl;
		
	Node<T>* cur = head;
	while (cur != NULL){
		cout << cur->data << " <-> ";
		cur = cur->next;
	}
}

/*int main(){
	DoublyLinkedList<int> List;
	
	int data, data2, data3, data4;
	cin >> data >> data2 >> data3 >> data4;
	List.PushBack(data);
	List.PushBack(data2);
	List.PushBack(data3);
	List.PushBack(data4);
	List.Delete(1);
	List.Print();
	
	return 0;
}*/
