#include <iostream>
#include <stack>
#include "ListGraph.h"
#include "ListGraph.cpp"
using namespace std;

template <typename T>
void DFS(T start, ListGraph<T> graph){
	stack<T> s; // 스택
	bool visit[graph.TotalVertex()] = { false }; // 노드에 방문했는지 체크하는 배열
	T seq[graph.TotalVertex()] = { 0 }; // 노드 방문 순서를 기록하는 배열
	
	int curIndex = graph.RetreiveIndex(start);
	T cur = start;
	s.push(cur);
	int pos = 1; // 해당 노드에 연결되어있는 노드들
	int sequence = 0; // 탐색 순서
	
	while (!s.empty()){
		seq[sequence] = s.top(); // 스택 최상단의 노드를 순서에 넣음
		sequence++;
		visit[curIndex] = true;
		
		while (true){
			if (visit[graph.RetreiveIndex(graph.RetreiveList(curIndex, pos))] != true){ // 방문하지 않은 노드일 경우 갱신함
				cur = graph.RetreiveList(curIndex, pos);
				s.push(cur);
				curIndex = graph.RetreiveIndex(s.top());
				break;
			}
			else{
				pos++;
				if (pos == graph.GetSize(curIndex)){
					s.pop(); // 인접리스트 내에 더이상 인접노드가 없는 경우 스택에서 노드 제거
					if (!s.empty()){ // 스택이 비지 않은 경우에 인덱스 최신화
						curIndex = graph.RetreiveIndex(s.top());
						pos = 1;
					}
					else// 아닌 경우 반복문 종료
						break;
				}
			}
		}
		
		pos = 1; // 인접리스트의 처음부터 다시 탐색
	}
	
	for (int i = 0; i < graph.TotalVertex(); i++)
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
	
	graph.Link(0, 1);
	graph.Link(0, 2);
	graph.Link(1, 6);
	graph.Link(3, 4);
	graph.Link(4, 5);
	
	DFS<int>(2, graph);
	
	return 0;
}*/
