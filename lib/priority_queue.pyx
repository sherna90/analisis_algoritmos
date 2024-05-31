# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False

from libcpp.queue cimport priority_queue


ctypedef unsigned long long ulong
ctypedef unsigned int uint

cdef extern from "pq.h" nogil:
    cdef cppclass CostIndex:
        float cost
        ulong address
        CostIndex()
        CostIndex(float cost, ulong index)


cdef class PyPQ:
    cdef priority_queue[CostIndex]* prio_q
    cdef uint count
    cdef items
    def __cinit__(self):
        self.prio_q = new priority_queue[CostIndex]()
        self.items = {}
        self.count = 0

    cpdef insert(self, tuple item):
        cdef CostIndex new_item = CostIndex(item[0], id(item[1]))
        self.prio_q.push(new_item)
        self.items[id(item[1])] = item[1]
        self.count += 1

    cpdef get_items(self):
        return list(self.items.values())

    cpdef empty(self):
        return self.count == 0

    cpdef size(self):
        return self.count

    cpdef pop(self):
        cdef CostIndex popped
        if not self.empty():
            popped = self.prio_q.top()
            self.prio_q.pop()
            cost = popped.cost
            item = self.items[popped.address]
            del self.items[popped.address]
            self.count -= 1
            return cost, item
        else:
            return None,None

    cpdef clear(self):
        while not self.empty():
            self.pop()

    def __dealloc__(self):

        del self.prio_q
