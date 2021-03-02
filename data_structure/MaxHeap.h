#ifndef ADDER_H 
#define ADDER_H
template <typename T>
class MaxHeap{
private:
	T* ary;
	T data;
	int size;
	
public:
	MaxHeap();
	~MaxHeap();
	
	bool IsEmpty() const;
	int GetSize() const;
	int Insert(const T& data);
	int Delete();
	void Swap(T* a, T* b);
	void Print();
};

#endif
