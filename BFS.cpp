#include <iostream>
#include <queue>
#include "ListGraph.h"
#include "ListGraph.cpp"
using namespace std;

template <typename T>
void BFS(T start, ListGraph<T> graph){
	queue<T> q;
	bool visit[graph.GetVertex()] = { false };
	T seq[graph.GetVertex()] = { 0 };
	
	int curIndex = graph.RetreiveIndex(start);
	T cur = start;
	q.push(cur);
	int pos = 1;
	int sequence = 0;
	int truevisit = 0;
	
	while(q.size() != 0){
		q.pop();
		if (visit[graph.RetreiveIndex(cur)] != true){ // 만일 해당 노드가 방문 노드가 아닐 경우 방문시킴!!! 아니면 그냥 단순 pop처리하고 끝!
			seq[sequence] = cur;
			sequence++;
			visit[curIndex] = true;
			truevisit++;
		}
		
		for (int i = 0; i < graph.GetSize(curIndex) - 1; i++){ // 방문하지 않은 인접 노드들을 큐에 추가시킴
			if (visit[graph.RetreiveIndex(graph.RetreiveList(curIndex, pos))] != true){
				cur = graph.RetreiveList(curIndex, pos);
				q.push(cur);
				pos++;
			}
			else
				pos++;
		}
		pos = 1; // 인접리스트의 탐색 위치 초기화
		
		cur = q.front();
		curIndex = graph.RetreiveIndex(cur); // 큐 앞의 노드들로 최신화!
	}
	
	for (int i = 0; i < truevisit; i++)
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
	
	BFS<int>(10, graph);
	
	return 0;
}
