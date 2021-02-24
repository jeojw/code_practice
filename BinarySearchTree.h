#ifndef ADDER_H 
#define ADDER_H

template <typename T>
struct Node{
	T data;
	Node<T>* left;
	Node<T>* right;
};

template <typename T>
class BinarySearchTree{
private:
	Node<T>* Root; // 최상위 노드
	
public:
	BinarySearchTree();
	~BinarySearchTree();
	
	int Insert(const T& data); // 삽입 함수
	int Delete(const T& data); // 삭제 함수
	Node<T>* Retreive(const T& data); // 노드 탐색 함수
	void Print(Node<T>* node); // 특정 노드 출력 함수
	void PrintAll(); // tree내 모든 노드를 출력하는 함수(전위 / 중위 / 후위 / 층별)
	void Preorder(Node<T>* node); // 전위 순회
	void Inorder(Node<T>* node); // 중위 순회
	void Postorder(Node<T>* node); // 후위 순회
	void Levelorder(Node<T>* node); //층별 순회
};

#endif
