#include <iostream>
#include "LinkedList.h"
using namespace std;

template <typename T>
LinkedList<T>::LinkedList(){
	head = NULL;
	tail = NULL;
	length = 0;
}

template <typename T>
LinkedList<T>::~LinkedList() {}

template <typename T>
bool LinkedList<T>::IsEmpty() const{
	if (length == 0)
		return true;
	else
		return false;
}

template <typename T>
int LinkedList<T>::GetLength() const{
	return length;
}

template <typename T>
int LinkedList<T>::PushBack(const T& data) {
	Node<T> *newNode = new Node<T>;
	newNode->data = data;
	newNode->next = NULL;
	
	if(length == 0)
		head = newNode;
	
	else	
		tail->next = newNode;
	
	tail = newNode;
	
	length++;
	
	return 1;
}

template <typename T>
int LinkedList<T>::Insert(const T& data, int Index) {
	Node<T> *newNode = new Node<T>;
	newNode->data = data;
	
	if ((length <= 1) || (Index == length)){
		cout << "Use PushBack!!" << endl;
		return -1;
	}
	
	if (Index > length){
		cout << "over the range!!!" << endl;
		return -1;
	}
	
	if (Index <= 0){
		cout << "Index Error!!" << endl;
		return -1;
	}
	
	if (Index == 1){ // 맨 앞에 수를 삽입시키는 함수.
		newNode->next = head;
		head = newNode;
		
		length++;
		
		return 1;
	}
	
	
	Node<T>* tmp = Search(Index - 1);
	newNode->next = tmp->next;
	tmp->next = newNode;
	
	length++;
	
	return 1;
}

template <typename T>
int LinkedList<T>::Pop() {
	if (length == 0){
		cout << "ERROR!!!" << endl;
		return -1;
	}
	Node<T>* Prev = Search(length - 1);
	Node<T>* del = Prev->next;
		
	Prev->next = NULL;
	delete del;
	Prev = tail;
		
	length--;
	
	return 1;
}

template <typename T>
int LinkedList<T>::Delete(int Index) {
	if (length == 0 || Index > length || Index <= 0){
		cout << "ERROR!!!" << endl;
		return -1;
	}
	
	if (Index == length){
		cout << "Use Pop!!!" << endl;
		return -1;
	}
	
	if (Index == 1){
		Node<T> *del = Search(1);
		head = Search(2);
		delete del;
		
		length--;
		return 1;
	}
	
	Node<T> *Prev = Search(Index - 1);
	Node<T>* del = Prev->next;
	
	Prev->next = Search(Index)->next;
	delete del;
	
	length--;
	return 1;
}

template <typename T>
Node<T>* LinkedList<T>::Search(int Index){
	Node<T> *cur = head;
	
	for (int i = 0; i < Index - 1; i++)
		cur = cur->next;
	
	return cur;
}

template <typename T>
void LinkedList<T>::Print(){
	if (length == 0)
		cout << "No Items!!" << endl;
	
	Node<T>* cur = head;
	while(cur != NULL){
		cout <<	cur->data << " -> ";
		cur = cur->next;
	}
}

/*int main(){
	int data, data2, data3, data4;
	cin >> data >> data2 >> data3 >> data4;
	LinkedList<int> List;
	List.PushBack(data);
	List.PushBack(data2);
	List.PushBack(data3);
	List.Insert(data4, 1);
	List.Print();
	
	return 0;
}*/
