# -*- coding: utf-8 -*-

"""
Iter ~ Built on the back of itertools, Iter allows easy list processing through chaining functions.

Example:
    Iter([1,2,3,4,5]).map(lambda x: x**2).top(2).collect() -> [25,16]
"""

__author__ = "Jason Liu"

from heapq import heapreplace, heapify

import itertools as it


class Iter(object):
    def __init__(self, iterable):
        self._iter = iterable

    def map(self, func):
        """
        Make an iterator that computes the function using arguments from each of the iterables.

        :rtype : Iter
        :param func, a -> b:
        :return:
        """
        return Iter(it.imap(func, self._iter))

    def flatmap(self, function_to_list):
        """
        Make an interator that returns elements from the lists produced by mapping function_to_list.

        :rtype : Iter
        :param function_to_list, a -> [b...]:
        :return:
        """
        return Iter(it.chain(self.map(function_to_list)._iter))

    def filter(self, predicate):
        """
        Make an iterator that filters elements from iterable returning only those for which the predicate is True.
        If predicate is None, return the items that are true.

        :rtype : Iter
        :param predicate, a -> bool:
        :return:
        """
        return Iter(it.ifilter(predicate, self._iter))

    def filterfalse(self, predicate):
        """
        Make an iterator that filters elements from iterable returning only those for which the predicate is False.
        If predicate is None, return the items that are false

        :rtype : Iter
        :param predicate, a -> bool:
        :return:
        """
        return Iter(it.ifilterfalse(predicate, self._iter))

    def takewhile(self, predicate):
        """
        Make an iterator that returns elements from the iterable as long as the predicate is true.

        :rtype : Iter
        :param predicate, a -> bool:
        :return:
        """
        return Iter(it.takewhile(predicate, self._iter))

    def dropwhile(self, predicate):
        """
        Make an iterator that drops elements from the iterable as long as the predicate is true;
        afterwards, returns every element.

        Note, the iterator does not produce any output until the predicate first becomes false,
        so it may have a lengthy start-up time.

        :rtype : Iter
        :param predicate, a -> bool:
        :return:
        """
        return Iter(it.dropwhile(predicate, self._iter))

    def groupby(self, keyfunc):
        """
        Make an iterator that returns consecutive keys and groups from the iterable.
        The key is a function computing a key value for each element.
        If not specified or is None, key defaults to an identity function and returns
        the element unchanged.

        :rtype : Iter
        :param keyfunc, a -> b:
        :return:
        """
        return Iter(it.groupby(keyfunc, self._iter))

    def chain(self, iterable):
        """Make an iterator that returns elements from the first iterable until it
        is exhausted, then proceeds to the next iterable, until all of the iterables
        are exhausted. Used for treating consecutive sequences as a single sequence.

        :type iterable: Iterable
        :rtype : Iter
        :param iterable:
        :return:
        """
        return Iter(it.chain(self._iter, iterable))

    def slice(self, *args):
        """
        Make an iterator that returns selected elements from the iterable. If start is non-zero, then elements from
        the iterable are skipped until start is reached. Afterward, elements are returned consecutively unless step is
        set higher than one which results in items being skipped. If stop is None, then iteration continues until the
        iterator is exhausted, if at all; otherwise, it stops at the specified position. Unlike regular slicing,
        slice() does not support negative values for start, stop, or step.

        :rtype : Iter
        :param args:
        :return:
        """
        return Iter(it.islice(self._iter, *args))

    def take(self, max):
        """
        Make and iterator that returns the first max elements from the original iterable

        :type max: int
        :param max:
        :return:
        """
        def func(iterable):
            for i, e in enumerate(iterable):
                if i < max:
                    yield e
        return Iter(func(self._iter))

    def sort(self, keyfunc=None):
        """
        Make and iterator that is sorted on a specific keyfunc, if keyfunc is None, sort on
        natural ordering.

        :rtype: Iter
        :param keyfunc:
        :return:
        """
        sorted_iterable = sorted(self._iter, (keyfunc or (lambda x: x)))

        def func(iterable):
            for i in iterable:
                yield i
        return Iter(func(sorted_iterable))

    def top(self, k=1, keyfunc=None):
        """
        Make an iterable of the top k elements of the original iterable sorted on keyfunc, if keyfunc is None sort
        on the natural ordering.

        :rtype: Iter
        :type k: int
        :param k:
        :return:
        """

        top_k_values = []

        if k == 1:
            return max(self._iter, key=(keyfunc or (lambda x: x)))

        for i, e in enumerate(self._iter):
            if i < k:
                top_k_values.append(e)
            elif i == k:
                heapify(top_k_values)
            else:
                heapreplace(top_k_values, e)

        return Iter(sorted(top_k_values, key=(keyfunc or (lambda x: x))))

    def count(self):
        """
        Counts all the elements of the original iterable

        :rtype: int
        :return:
        """
        return len(self._iter)

    def distinct(self):
        """
        Return only the distinct elements of the iterable.

        :return:
        """

        def func(iterable):
            # This iterator simply puts elements into a set and looks for
            # simple set membership. Bloom filter implementation may be of interest
            distinct_values = set()
            for i in iterable:
                if i not in distinct_values:
                    distinct_values.add(i)
                    yield i
        return Iter(func(self._iter))

    def collect(self):
        """
        Collect the iterable back into a list.

        :return:
        """
        return list(self._iter)

    def __iter__(self):
        return self._iter
