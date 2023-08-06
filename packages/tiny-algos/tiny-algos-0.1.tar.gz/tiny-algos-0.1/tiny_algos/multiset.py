from itertools import chain


class MultiSet:
    def __init__(self, iterable=None):
        self._dict = {}
        self._len = 0
        self._min = None
        self._max = None
        self._min_changed = False
        self._max_changed = False
        if iterable:
            iterable = list(iterable)
            for value in iterable:
                self._add(value)
            self._len = len(iterable)
            if iterable is not None:
                self._min = min(iterable)
                self._max = max(iterable)

    def _add(self, value):
        if value not in self._dict:
            self._dict[value] = 0
        self._dict[value] += 1

    def add(self, value):
        self._add(value)
        if not self._min_changed:
            if self._min is not None:
                self._min = min(self._min, value)
            else:
                self._min = value
        if not self._max_changed:
            if self._max is not None:
                self._max = max(self._max, value)
            else:
                self._max = value
        self._len += 1

    def _remove(self, value):
        self._dict[value] -= 1
        if self._dict[value] == 0:
            del self._dict[value]

    def remove(self, value):
        self._remove(value)
        if not self._dict:
            self._min = None
            self._max = None
        elif value not in self._dict:
            if self._min == value:
                self._min_changed = True
                self._min = None
            if self._max == value:
                self._max_changed = True
                self._max = None
        self._len -= 1

    @property
    def min(self):
        if self._min_changed:
            self._min = min(self._dict)
        self._min_changed = False
        return self._min

    @property
    def max(self):
        if self._max_changed:
            self._max = max(self._dict)
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
