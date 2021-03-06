#include "ListGraph.h"
#include <algorithm>
using namespace std;

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
T ListGraph<T>::GetHeader(int Index) const{
	return List[Index][0];
}

template <typename T>
int ListGraph<T>::GetSize(int Index) const{
	return List[Index].size();
}

template <typename T>
T ListGraph<T>::RetreiveList(int Index1, int Index2){
	return List[Index1][Index2];
}

template <typename T>
int ListGraph<T>::RetreiveIndex(const T& data){
	for (int i = 0; i < List.size(); i++){
		if (List[i][0] == data)
			return i;
	}
	
	return 1;
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
int ListGraph<T>::LinkVertex(int Index1, int Index2){
	List[Index1].push_back(List[Index2][0]);
	List[Index2].push_back(List[Index1][0]);
	
	List[Index1].erase(unique(List[Index1].begin(), List[Index1].end()),List[Index1].end()); // 무방향 그래프이므로 쌍방향으로 연결 한 후 중복요소 제거!!
	List[Index2].erase(unique(List[Index2].begin(), List[Index2].end()),List[Index2].end());
		
	return 1;
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
