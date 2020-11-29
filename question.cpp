#include <iostream>
using namespace std;

template <typename T>
struct Node{
	T data; //노드 내의 데이터
	Node<T> *next; // 다음 노드의 주소값
};

template <typename T>
class LinkedList{
private:
	Node<T> *head; // 리스트의 첫번째 노드
	Node<T> *tail; // 리스트의 마지막 노드
	int length; // 리스트의 전체 길이
	
public:
	LinkedList();
	~LinkedList();
	
	bool IsEmpty() const; // 리스트가 비어있는지 판별하는 함수
	int GetLength() const; //리스트의 크기를 반환하는 함수
	int PushBack(const T& data); // 리스트 마지막에 노드를 추가함
	int Insert(const T& data, int Index); //리스트 중간에 노드를 추가함-> Index는 리스트에 추가시키고 싶은 위치
	int Pop(); // 마지막 노드 삭제 함수
	int Delete(int Index); // 노드 삭제 함수
	void Search() const; // 노드를 탐색하는 함수
	void Print(); //리스트 전체를 출력하는 함수
};

template <typename T>
LinkedList<T>::LinkedList(){
	head = new Node<T>;
	tail = new Node<T>;
	head = NULL;
	length = 0;
}

template <typename T>
LinkedList<T>::~LinkedList() {
	delete head;
	delete tail;
}

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
	if(length <= 1){
		cout << "Use PushBack!!" << endl;
	}
	else{
		Node<T> *newNode = new Node<T>;
		Node<T> *Prev = new Node<T>;
		Node<T> *Next = new Node<T>;
		
	}
	
	length++;
	
	return 1;
}

template <typename T>
int LinkedList<T>::Pop() {
	if (length == 0){
		cout << "ERROR!!!" << endl;
		return -1;
	}
	else{
		
	}
}

template <typename T>
int LinkedList<T>::Delete(int Index) {
	
}

template <typename T>
void LinkedList<T>::Search() const{
	
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

int main(){
	int data, data2, data3;
	cin >> data >> data2 >> data3;
	LinkedList<int> List;
	List.PushBack(data);
	List.PushBack(data2);
	List.PushBack(data3);
	List.Print();
	
	return 0;
}
