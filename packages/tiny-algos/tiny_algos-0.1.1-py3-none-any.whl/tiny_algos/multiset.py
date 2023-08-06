from itertools import chain
from collections import defaultdict

PINF = 9223372036854775807  # 2 ** 63 - 1
NINF = -PINF
MIN_DEFAULT = PINF
MAX_DEFAULT = NINF


class MultiSet:
    def __init__(self, iterable=None):
        self._dict = defaultdict(int)
        self._len = 0
        self._min = MIN_DEFAULT
        self._max = MAX_DEFAULT
        self._min_changed = False
        self._max_changed = False
        if iterable is not None:
            iterable = list(iterable)
            for value in iterable:
                self._dict[value] += 1
            self._len = len(iterable)
            self._min = min(iterable, default=self._min)
            self._max = max(iterable, default=self._max)

    def add(self, value):
        self._dict[value] += 1
        if not self._min_changed:
            self._min = min(self._min, value)
        if not self._max_changed:
            self._max = max(self._max, value)
        self._len += 1

    def remove(self, value):
        if value in self._dict and self._dict[value] > 1:
            self._dict[value] -= 1
        else:
            del self._dict[value]

        if value not in self._dict:
            if self._min == value:
                self._min_changed = True
            if self._max == value:
                self._max_changed = True

        self._len -= 1

    @property
    def min(self):
        if self._min_changed:
            self._min = min(self._dict, default=MIN_DEFAULT)
            self._min_changed = False
        return self._min

    @property
    def max(self):
        if self._max_changed:
            self._max = max(self._dict, default=MAX_DEFAULT)
            self._max_changed = False
        return self._max

    def __len__(self):
        return self._len

    def __contains__(self, value):
        return value in self._dict

    def __repr__(self):
        return f"""MultiSet({
            list(chain.from_iterable([k] * v for k, v in self._dict.items()))
        })"""
