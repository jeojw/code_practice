#ifndef ADDER_H 
#define ADDER_H

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

#endif
