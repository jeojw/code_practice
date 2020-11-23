#include <iostream>
using namespace std;

template <typename T>
struct Node{
	T data; //노드 내의 데이터
	Node<T> *next; // 노드의 주소값
}

template <typename T>
class LinkedList{
private:
	Node<T> *head; // 리스트의 첫번째 노드
	Node<T> *tail; // 리스트의 마지막 노드
	int length = 0; // 리스트의 전체 길이
	
public:
	LinkedList();
	~LinkedList();
	
	bool empty() const; // 리스트가 비어있는지 판별하는 함수
	int PushBack(T data) const; // 리스트 마지막에 노드를 추가함
	int insert(T data, int Index) const; //리스트 중간에 노드를 추가함->
	int Pop() const; // 마지막 노드 삭제 함수
	int Delete() const; // 노드 삭제 함수
	void Search() const; // 노드를 탐색하는 함수
	void Print(); //리스트 전체를 출력하는 함수
	int GetLength(); //리스트의 크기를 반환하는 함수
}

template <typename T>
LinkedList<T>::LinkedList(){
	head = NULL;
}

template <typename T>
LinkedList<T>::~LinkedList() {}

template <typename T>
bool LinkedList<T>::empty() const{
	if (length == 0)
		return true;
	else
		return false;
}

template <typename T>
int LinkedList<T>::PushBack(T data) const{
	if(length == 0){
		head->data = data;
		head->next = NULL;
	}
	else{
		Node<T> *newNode = new Node<T>;
		
		newNode->data = data;
		newNode->next = NULL;
		
		tail->next = newNode;
	}
	
	length++;
	return 1;
}

template <typename T>
int LinkedList<T>::Insert(T data, int Index){
	if(length == 0){
		head->data = data;
		head->next = NULL;
	}
	else{
		Node<T> *newNode = new Node<T>;
		
		
	}
}

template <typename T>
int LinkedList<T>::Pop() const{
	if (length == 0){
		cout << "ERROR!!!" << endl;
		return -1;
	}
	else{
		
	}
}

template <typename T>
int LinkedList<T>::Delete() const{
	
}

template <typename T>
void LinkedList<T>::Search() const{
	
}

template <typename T>
void LinkedList<T>::Print(){
	
}

int main(){
	
	return 0;
}
