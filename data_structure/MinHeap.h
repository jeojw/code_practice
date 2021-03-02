#ifndef ADDER_H 
#define ADDER_H
template <typename T>
class MinHeap{
private:
	T* ary;
	T data;
	int size;
	
public:
	MinHeap();
	~MinHeap();
	
	bool IsEmpty() const;
	int GetSize() const;
	int Insert(const T& data);
	int Delete();
	void Swap(T* a, T* b);
	void Print();
};

#endif
