#include <iostream>
#define MAX 100
using namespace std;

template <typename T>
struct Node{
	T data;
	Node<T>* link;
};

template <typename T>
class ListGraph{
private:
	Node<T>* List;
	int edges;
	int vertexs;
	
public:
	ListGraph();
	~ListGraph();
	
	int GetEdge() const;
	int GetVertex() const;
	int PushVertex(const T& data, int Index); // 정점을 추가시키는 함수
	int LinkVertex();
	void PrintVertex();
};

template <typename T>
ListGraph<T>::ListGraph(){
	List = new Node<T>[MAX];
	edges = 0;
	vertexs = 0;
}

template <typename T>
ListGraph<T>::~ListGraph(){
	delete[] List;
}

template <typename T>
int ListGraph<T>::GetEdge() const{
	return edges;
}

template <typename T>
int ListGraph<T>::GetVertex() const{
	return vertexs;
}

template <typename T>
int ListGraph<T>::PushVertex(const T& data, int Index){
	Node<T>* Vertex = new Node<T>;
	Vertex->data = data;
	
	List[Index] = Vertex;
	vertexs++;
}

template <typename T>
void ListGraph<T>::PrintVertex(){
	for (int i = 0; i < vertexs; i++)
		cout << List[i] << " ";
}

int main(){
	ListGraph<int> graph;
	
	graph.PushVertex(4, 0);
	graph.PushVertex(7, 1);
	graph.PushVertex(3, 2);
	graph.PushVertex(6, 3);
	graph.PushVertex(8, 4);
	graph.PrintVertex();
	
	return 0;
}
