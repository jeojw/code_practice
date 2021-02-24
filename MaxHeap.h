#include <iostream>
#include "BinarySearchTree.h"
using namespace std;

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
		
		if (data < parent->data)
			parent->left = newNode;
		
		else
			parent->right = newNode;
	}
	
	return 1;
}

template <typename T>
int BinarySearchTree<T>::Delete(const T& data){
	Node<T>* cur = Root;
	Node<T>* parent;
	
	while (data != cur->data){
		parent = cur;
		
		if (data < cur->data)
			cur = cur->left;
		else
			cur = cur->right;
	}
	
	Node<T>* del = cur;
	
	if (del->left == NULL && del->right == NULL){
		if (parent->left == del){
			parent->left = NULL;
			delete del;
			return 1;
		}
		
		if (parent->right == del){
			parent->right = NULL;
			delete del;
			return 1;
		}
	}
	
	if (del->left != NULL && del->right == NULL){
		if (parent->left == del){
			parent->left = del->left;
			delete del;
			return 1;
		}
		
		if (parent->right == del){
			parent->right = del->left;
			delete del;
			return 1;
		}
	}
	
	if (del->left == NULL && del->right != NULL){
		if (parent->left == del){
			parent->left = del->right;
			delete del;
			return 1;
		}
		
		if (parent->right == del){
			parent->right = del->right;
			delete del;
			return 1;
		}
	}
	
	if (del->left != NULL && del->right != NULL){
		if (parent->left == del){
			parent->left = del->right;
			(del->right)->left = del->left;
			delete del;
			return 1;
		}
		
		if (parent->right == del){
			parent->right = del->left;
			(del->left)->right = del->right;
			delete del;
			return 1;
		}
	}
	
	return 0;
}

template <typename T>
Node<T>* BinarySearchTree<T>::Retreive(const T& data){
	Node<T>* cur = Root;
	Node<T>* parent;
	
	while (cur != NULL){
		if (data == cur->data)
			return cur;
		
		parent = cur;
		
		if (data > cur->data)
			cur = cur->right;
		else
			cur = cur->left;
	}
	
	if (cur == NULL){
		cout << "No data!!" << endl;
		return NULL;
	}
}

template <typename T>
void BinarySearchTree<T>::Print(Node<T>* node){
	cout << node->data << " -> ";
}

template <typename T>
void BinarySearchTree<T>::PrintAll(){
	cout << "Preorder: ";
	Preorder(Root);
	cout << endl;
	cout << "Inorder: ";
	Inorder(Root);
	cout << endl;
	cout << "Postorder: ";
	Postorder(Root);
}

template <typename T>
void BinarySearchTree<T>::Preorder(Node<T>* node){
	if (node == NULL)
		return;
	
	Print(node);
	Preorder(node->left);
	Preorder(node->right);
}

template <typename T>
void BinarySearchTree<T>::Inorder(Node<T>* node){
	if (node == NULL)
		return;
	
	Inorder(node->left);
	Print(node);
	Inorder(node->right);
}

template <typename T>
void BinarySearchTree<T>::Postorder(Node<T>* node){
	if (node == NULL)
		return;
	
	Postorder(node->left);
	Postorder(node->right);
	Print(node);
}

template <typename T>
void BinarySearchTree<T>::Levelorder(Node<T>* node){
	
}

/*int main(){
	BinarySearchTree<int> Tree;
	
	Tree.Insert(5);
	Tree.Insert(6);
	Tree.Insert(3);
	Tree.Insert(4);
	Tree.Insert(7);
	Tree.Insert(1);
	Tree.Delete(5);
	Tree.PrintAll();

	return 0;
}*/
