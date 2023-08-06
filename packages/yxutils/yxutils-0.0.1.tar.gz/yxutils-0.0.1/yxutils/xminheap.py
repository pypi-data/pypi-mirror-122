import heapq


class xminheap:
    def __init__(self, maxorder=2**30, sortkey=None, recoverkey=None):
        self.__heap = []
        self.__maxorder = maxorder if maxorder > 0 else 1
        self.__maxval = None
        self.__sortkey = sortkey
        self.__recoverkey = recoverkey

    def push(self, x):
        if len(self.__heap) < self.__maxorder or (
                self.__sortkey and self.__sortkey(x) < self.__sortkey(
                    self.__maxval)) or x < self.__maxval:
            heapq.heappush(self.__heap,
                           x if not self.__sortkey else self.__sortkey(x))
            self.__maxval = x if not self.__sortkey else self.__sortkey(x)

    def getheap(self):
        if not self.__recoverkey:
            return self.__heap
        else:
            return [self.__recoverkey(x) for x in self.__heap]

    def first(self):
        if self.__recoverykey:
            return self__recoverkey(self.__heap[0]) if len(
                self.__heap) else None
        return self.__heap[0] if len(self.__heap) else None


if __name__ == "__main__":
    minh = xminheap(5, sortkey=lambda x: -x, recoverkey=lambda x: -x)
    #minh = xminheap(5,sortkey=lambda x:x)
    minh.push(1)
    print(minh.getheap())
    minh.push(5)
    print(minh.getheap())
    minh.push(4)
    print(minh.getheap())
    minh.push(-1)
    print(minh.getheap())
    minh.push(9)
    print(minh.getheap())
    minh.push(-5)
    print(minh.getheap())
    minh.push(8)
    print(minh.getheap())
    minh.push(5)
    print(minh.getheap())
    minh.push(-9)
    print(minh.getheap())
