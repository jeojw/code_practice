#ifndef ADDER_H 
#define ADDER_H

template <typename T>
struct Node{
	T data;
	Node<T>* next;
	Node<T>* prev;
};

template <typename T>
class DoublyLinkedList{
private:
	Node<T>* head;
	Node<T>* tail;
	int length;
	
public:
	DoublyLinkedList();
	~DoublyLinkedList();
	
	bool IsEmpty() const;
	int GetLength() const;
	int PushBack(const T& data);
	int Insert(const T& data, int Index);
	int Pop();
	int Delete(int Index);
	Node<T>* Search(int Index);
	void Print();
};

#endif
