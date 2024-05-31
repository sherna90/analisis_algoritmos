#ifndef PQ
#define PQ
#include <ostream>

//typedef unsigned long long ulong;

class  CostIndex{
public:
	float cost;
	unsigned long long address;

	CostIndex(){
		cost = 0;
		address = 0;
	}

	CostIndex(float cost, unsigned long long address) : cost(cost), address(address){};
	
	bool operator<(const CostIndex &rhs) const{
		return (cost > rhs.cost);
	}

	bool operator>(const CostIndex &rhs) const{
		return (cost < rhs.cost);
	}

	bool operator==(const CostIndex &rhs) const{
		return (cost == rhs.cost && address == rhs.address);
	}

	bool operator!=(const CostIndex &rhs) const{
		return (cost != rhs.cost || address != rhs.address);
	}

};

std::ostream& operator<<(std::ostream& os, CostIndex& obj){
	return os << "{cost: " << obj.cost << ", index: " << obj.address << "}"<< std::endl;

}



#endif