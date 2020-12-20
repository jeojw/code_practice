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
	
	int GetEdge() const; // 그래프의 총 간선 개수
	int GetVertex() const; // 그래프의 총 정점 개수
	T GetHeader(int Index) const; // 그래프 헤더정점을 반환하는 함수
	int GetSize(int Index) const; // 각 인접리스트의 크기를 반환하는 함수
	T RetreiveList(int Index1, int Index2); // 각 인접리스트의 요소를 반환하는 함수
	int PushHeader(const T& data); // 정점을 추가시키는 함수
	int LinkVertex(int Index1, int Index2); // 헤더정점에서 갈 수 있는 정점을 추가시키는 함수
	void PrintAll(); // 그래프 형태를 전원 출력시키는 함수
};

#endif
