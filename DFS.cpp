#include <iostream>
#include <stack>
#include "ListGraph.h"
#include "ListGraph.cpp"
using namespace std;

template <typename T>
void DFS(T start, ListGraph<T> graph){
	stack<T> s; // 스택
	bool visit[graph.GetVertex()] = { false }; // 노드에 방문했는지 체크하는 배열
	T seq[graph.GetVertex()]; // 노드 방문 순서를 기록하는 배열
	
	int curIndex = graph.RetreiveIndex(start);
	visit[curIndex] = true;
	T cur = start;
	s.push(cur);
	int pos = 1; // 해당 노드에 연결되어있는 노드들
	int sequence = 0; // 탐색 순서
	int truevisit = 1; // 총 방문한 노드 개수
	seq[sequence] = cur;
	
	while (truevisit != graph.GetVertex()){
		while (true){
			if (visit[graph.RetreiveIndex(graph.RetreiveList(curIndex, pos))] == true){ // 해당 노드에 이미 방문했을경우 다른 인접노드 방문 및 백트래킹
				pos++;
				if (pos == graph.GetSize(curIndex)){
					s.pop();
					curIndex = graph.RetreiveIndex(s.top());
					pos = 1;
				}
			}
			
			else{ // 노드 방문 성공 및 위의 변수들 갱신
				cur = graph.RetreiveList(curIndex, pos);
				curIndex = graph.RetreiveIndex(cur);
				s.push(cur);
				visit[curIndex] = true;
				pos = 1;
				sequence++;
				seq[sequence] = cur;
				truevisit++;
				break;
			}
		}
	}
	int size = s.size();
	for (int i = 0; i < size; i++) // 스택 내의 모든 요소를 제거함으로써 탐색 종료
		s.pop();
	
	for (int i = 0; i < truevisit; i++)
		cout << seq[i] << "->";
}

/*int main(){
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
	
	DFS<int>(8, graph);
	
	return 0;
}*/
