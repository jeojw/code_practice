#i#include <iostream>
#include "ListGraph.h"
#include "ListGraph.cpp"
#include <stack>
using namespace std;

template <typename T>
void DFS(int Index, ListGraph<T> graph){
	stack<T> s;
	bool visit[graph.GetVertex()] = { false };
	T seq[graph.GetVertex()]; // 노드 방문 순서를 기록하는 배열
	
	visit[Index] = true;
	T cur = graph.GetHeader(Index);
	s.push(cur);
	int curIndex = Index;
	int pos = 1;
	int sequence = 0;
	int pIndex;
	seq[sequence] = cur;
	
	while (true){
		while (true){
			if (visit[graph.RetreiveIndex(graph.RetreiveList(curIndex, pos))] == true){
				pos++;
				if (pos == graph.GetSize(curIndex)){
					curIndex = pIndex;
				}
			}
			
			else{
				cur = graph.RetreiveList(curIndex, pos);
				pIndex = curIndex;
				curIndex = graph.RetreiveIndex(cur);
				s.push(cur);
				visit[curIndex] = true;
				pos = 1;
				sequence++;
				seq[sequence] = cur;
				break;
			}
		}
		
		if (s.size() == graph.GetVertex())
			break;
		else
			continue;
	}
	
	for (int i = 0; i < s.size(); i++)
		cout << seq[i] << "->";
}

int main(){
	ListGraph<int> graph;
	
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
	
	DFS<int>(0, graph);
	
	return 0;
}
