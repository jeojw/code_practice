#include <iostream>
#include "ListGraph.h"
#include "Stack.h"
using namespace std;

/*template <typename T>
void DFS(ListGraph<T> graph, Stack<T> stack){
	bool visit[graph.HeaderSize()] = false;
	int Index = 0;
	
	while (Index != graph.HeaderSize() - 1){
		visit[Index] = true;
		for (int i = 0; i < graph.GetSize(Index); i++)
			stack.Push(graph.RetreiveList[Index][i]);
		
		for (int i = 0; i < graph.GetSize(Index); i++){
			if (link)
		}
	}
	
}*/

int main(){
	ListGraph<int> graph;
//	Stack<int> stack;
	
	graph.PushHeader(2);
	graph.PushHeader(4);
	graph.PushHeader(5);
	graph.PushHeader(6);
	graph.PushHeader(7);
	graph.PushHeader(8);
	graph.PushHeader(10);
	
	graph.LinkVertex(0, 1);
	graph.LinkVertex(0, 2);
	graph.LinkVertex(0, 6);
	graph.LinkVertex(1, 3);
	graph.LinkVertex(2, 5);
	graph.LinkVertex(3, 4);
	graph.LinkVertex(3, 5);
	graph.LinkVertex(5, 6);
	graph.LinkVertex(6, 1);
	graph.PrintAll();
	
//	DFS<int>(graph, stack);
	
	return 0;
}
