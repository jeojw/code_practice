#include <iostream>
using namespace std;

template <typename T>
struct Node{
	T data; //노드 내의 데이터
	Node<T> *next; // 다음 노드의 주소를 저장할 포인터(절대!!! 자기 자신이 아님!!!!!!)
};

template <typename T>
class LinkedList{
private:
	Node<T> *head; // 리스트의 첫번째 노드
	Node<T> *tail; // 리스트의 마지막 노드
	int length; // 리스트의 전체 길이
	
public:
	LinkedList(); // 생성자
	~LinkedList(); // 소멸자
	
	bool IsEmpty() const; // 리스트가 비어있는지 판별하는 함수
	int GetLength() const; // 리스트의 크기를 반환하는 함수
	int PushBack(const T& data); // 리스트 마지막에 노드를 추가함
	int Insert(const T& data, int Index); // 리스트 중간에 노드를 추가함
	int Pop(); // 마지막 노드 삭제 함수
	int Delete(int Index); // 노드 삭제 함수
	Node<T>* Search(int Index); // 노드를 탐색하는 함수, index는 리스트 내의 노드의 좌표값(1부터 시작.....)
	void Print(); // 리스트 전체를 출력하는 함수
};

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
	
	if (Index == 1){ // 맨 앞에 수를 삽입시키는 함수.
		newNode->next = Search(1);
		int cur = 1;
		while (cur != length){
			Search(cur)->next = Search(cur + 1);
			cur++;
		}
		
		head = newNode;
		tail = Search(length);
		
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
	Node<T>* del = Search(length);
		
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
	Node<T> *del = Search(Index);
	
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

int main(){
	int data, data2, data3, data4;
	cin >> data >> data2 >> data3 >> data4;
	LinkedList<int> List;
	List.PushBack(data);
	List.PushBack(data2);
	List.PushBack(data3);
	List.Insert(data4, 2);
	List.Delete(1);
	List.Print();
	
	return 0;
}
