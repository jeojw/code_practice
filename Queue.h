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
class Queue{
private:
	Node<T>* Front; // 큐의 맨 앞의 인덱스
	Node<T>* Rear; // 큐의 맨 뒤의 인덱스
	int size; // 큐의 크기

public:
	Queue();
	~Queue();
	
	int GetSize() const; // 큐의 사이즈를 반환
	bool IsEmpty() const; // 큐가 비어있는지 확인하는 함수
	int Enqueue(const T& data); // 큐 맨 뒤에 요소를 추가하는 함수
	int Dequeue(); // 큐 맨 앞에 요소를 지우는 함수
	int Peek(); // front에 위치한 데이터를 읽는 함수
	void Print(); // 큐에 들어있는 원소들을 전원 출력하는 함수
};

#endif
