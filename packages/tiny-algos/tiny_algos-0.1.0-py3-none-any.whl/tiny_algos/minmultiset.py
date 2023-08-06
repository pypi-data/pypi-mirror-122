from heapq import heapify, heappop, heappush

PINF = 9223372036854775807  # 2 ** 63 - 1
NINF = -PINF
MIN_DEFAULT = PINF
MAX_DEFAULT = NINF


class MinMultiSet:
    def __init__(self, iterable=None, remove_iterable=None):
        self._list = []
        self._remove_list = []

        if iterable:
            self._list = list(iterable)
            heapify(self._list)
        if remove_iterable:
            self._remove_list = list(remove_iterable)
            heapify(self._remove_list)

    def sanitize(self):
        while (
            self._list and self._remove_list and self._list[0] == self._remove_list[0]
        ):
            heappop(self._list)
            heappop(self._remove_list)

    def add(self, value):
        if self._remove_list and self._remove_list[0] == value:
            heappop(self._remove_list)
            self.sanitize()
        else:
            heappush(self._list, value)

    def remove(self, value):
        if self._list and self._list[0] == value:
            heappop(self._list)
            self.sanitize()
        else:
            heappush(self._remove_list, value)

    @property
    def min(self):
        self.sanitize()
        if self._list:
            return self._list[0]
        else:
            return MIN_DEFAULT

    def __len__(self):
        return len(self._list) - len(self._remove_list)

    def __repr__(self):
        return (
            f"MinMultiSet(iterable={self._list}, "
            f"remove_iterable={self._remove_list})"
        )


class MaxMultiSet:
    def __init__(self, iterable=None, remove_iterable=None, minms=None):
        if minms is None:
            inv_iterable = []
            inv_remove_iterable = []
            if iterable:
                inv_iterable = (-v for v in iterable)
            if remove_iterable:
                inv_remove_iterable = (-v for v in remove_iterable)
            minms = MinMultiSet(inv_iterable, inv_remove_iterable)

        self._minms = minms

    def add(self, value):
        self._minms.add(-value)

    def remove(self, value):
        self._minms.remove(-value)

    @property
    def max(self):
        return -self._minms.min

    def __len__(self):
        return len(self._minms)

    def __repr__(self):
        return f"MaxMultiSet(minms={self._minms})"
