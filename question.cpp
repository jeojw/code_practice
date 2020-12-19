#include <iostream>
#include "ListGraph.h"
#include "Stack.h"
using namespace std;

/*template <typename T>
void DFS(ListGraph<T> graph, Stack<T> stack){
	int visit[];
	stack.Push(graph.GetHeader(0))
}*/

int main(){
	ListGraph<int> graph;
//	Stack<int> stack;
	
	graph.PushHeader(4);
	graph.PushHeader(7);
	graph.PushHeader(3);
	graph.PushHeader(6);
	graph.PushHeader(8);
	graph.LinkVertex(0, 7);
	graph.LinkVertex(0, 3);
	graph.LinkVertex(1, 6);
	graph.LinkVertex(2, 8);
	graph.LinkVertex(3, 8);
	graph.LinkVertex(3, 4);
	graph.LinkVertex(4, 7);
	graph.PrintAll();
	
//	void DFS(graph, stack);
	
	return 0;
}
///////////////////////////////////////////////////////

#ifndef ADDER_H 
#define ADDER_H
#include <iostream>
#include <vector>
using namespace std;

template <typename T>
class ListGraph{
private:
	vector< vector<T> > List;
	int edges;
	int vertexs;
	
public:
	ListGraph();
	~ListGraph();
	
	int GetEdge() const;
	int GetVertex() const;
	int GetHeader(int Index) const;
	int GetSize(int Index) const;
	int RetreiveList(int Index1, int Index2);
	int PushHeader(const T& data); // 정점을 추가시키는 함수
	int LinkVertex(int Index, const T& data);
	void PrintAll();
};

#endif

///////////////////////////////////////////////////////////////////////

#include "ListGraph.h"

template <typename T>
ListGraph<T>::ListGraph(){
	edges = 0;
	vertexs = 0;
}

template <typename T>
ListGraph<T>::~ListGraph(){}

template <typename T>
int ListGraph<T>::GetEdge() const{
	return edges;
}

template <typename T>
int ListGraph<T>::GetVertex() const{
	return vertexs;
}

template <typename T>
int ListGraph<T>::GetHeader(int Index) const{
	return List[Index][0];
}

template <typename T>
int ListGraph<T>::GetSize(int Index) const{
	return List[Index].size();
}

template <typename T>
int ListGraph<T>::RetreiveList(int Index1, int Index2){
	return List[Index1][Index2];
}

template <typename T>
int ListGraph<T>::PushHeader(const T& data){
	vector<T> headlist;
	headlist.push_back(data);
	List.push_back(headlist);
	vertexs++;
	
	return 1;
}

template <typename T>
int ListGraph<T>::LinkVertex(int Index, const T& data){
	for (int i = 0; i < List.size(); i++){
		if (List[i][0] != data)
			continue;
		
		else{
			List[Index].push_back(data);
			edges++;
			
			return 1;
		}
	}
}

template <typename T>
void ListGraph<T>::PrintAll(){
	for (int i = 0; i < List.size(); i++){
		for (int j = 0; j < List[i].size(); j++){
			cout << List[i][j] << "->";
		}
		cout << endl << "↓" << endl;
	}
}
