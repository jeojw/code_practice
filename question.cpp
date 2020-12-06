#include <iostream>
using namespace std;

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
	void Preorder(); // 전위 순회
	void Inorder(); // 중위 순회
	void Postorder(); // 후위 순회
	void Levelorder(); //층별 순회
};

template <typename T>
BinarySearchTree<T>::BinarySearchTree(){
	Root = NULL;
}

template <typename T>
BinarySearchTree<T>::~BinarySearchTree(){}

template <typename T>
int BinarySearchTree<T>::Insert(const T& data){
	Node<T>* newNode = new Node<T>;
	newNode->data = data;
	newNode->left = NULL;
	newNode->right = NULL;
	
	if (Root == NULL)
		Root = newNode;
	
	else{
		Node<T>* parent;
		Node<T>* cur = Root;
		
		while (cur != NULL){
			if (data == cur->data)
				throw std::runtime_error("data is already existed. data : " + std::to_string(data));
			
			parent = cur;
			
			if (data < cur->data)
				cur = cur->left;
			
			else
				cur = cur->right;
		}
		
		if (data < cur->data)
			cur->left = newNode;
		
		else
			cur->right = newNode;
	}
	
	return 1;
}

template <typename T>
int BinarySearchTree<T>::Delete(const T& data){
	Node<T>* del = Retreive(data);
	Node<T>* parent;
	
	if (del->left == NULL && del->right == NULL){
		
	}
	
	if (del->left != NULL && del->right == NULL){
		
	}
	
	if (del->left == NULL && del->rigt != NULL){
		
	}
	
	if (del->left != NULL && del->right != NULL){
		
	}
	
	return 0;
}

template <typename T>
Node<T>* BinarySearchTree<T>::Retreive(const T& data){
	Node<T>* cur = Root;
	Node<T>* parent;
	
	while(cur->data != data){
		parent = cur;
		
		if (cur->data < data)
			cur = cur->left;
		
		else
			cur = cur->right;
	}
	
	return cur;
}

template <typename T>
void BinarySearchTree<T>::Preorder(){

}

int main(){
	BinarySearchTree<int> Tree;
	
	Tree.Insert(5);
	Tree.Insert(6);
	Tree.Insert(3);
	Tree.Insert(4);
	Tree.Insert(7);
	
	return 0;
}
