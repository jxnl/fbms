# -*- coding: utf-8 -*-

"""
Iter ~ Built on the back of itertools, Iter allows easy list processing through chaining functions.

Example:
    Iter([1,2,3,4,5]).map(lambda x: x**2).top(2).collect() -> [25,16]
"""

__author__ = "Jason Liu"

from copy import deepcopy
from heapq import heapreplace, heapify
from collections import defaultdict

import itertools as it


class Iter(object):
    def __init__(self, iterable):
        self._iter = iterable

    def map(self, func):
        """
        Make an iterator that computes the function using arguments from each of the iterables.

        :param func, a -> b:
        :return:
        """
        return Iter(it.imap(func, self._iter))

    def flatmap(self, function_to_list):
        """
        Make an interator that returns elements from the lists produced by mapping function_to_list.

        :param function_to_list, a -> [b...]:
        :return:
        """
        return Iter(it.chain(self.map(function_to_list)._iter))

    def filter(self, predicate):
        """
        Make an iterator that filters elements from iterable returning only those for which the predicate is True.
        If predicate is None, return the items that are true.

        :param predicate, a -> bool:
        :return:
        """
        return Iter(it.ifilter(predicate, self._iter))

    def filterfalse(self, predicate):
        """
        Make an iterator that filters elements from iterable returning only those for which the predicate is False.
        If predicate is None, return the items that are false

        :param predicate, a -> bool:
        :return:
        """
        return Iter(it.ifilterfalse(predicate, self._iter))

    def takewhile(self, predicate):
        """
        Make an iterator that returns elements from the iterable as long as the predicate is true.

        :param predicate, a -> bool:
        :return:
        """
        return Iter(it.takewhile(predicate, self._iter))

    def dropwhile(self, predicate):
        """
        Make an iterator that drops elements from the iterable as long as the predicate is true

        Note, the iterator does not produce any output until the predicate first becomes false,
        so it may have a lengthy start-up time.

        :param predicate:
        :return:
        """
        return Iter(it.dropwhile(predicate, self._iter))

    def groupby(self, keyfunc=None, valfunc=None):
        """
        Make an iterator that returns consecutive keys and groups from the iterable.
        The key and value is computed each element by keyfunc and valfunc.
        If these functions are not not specified or is None, they default to identity function.

        :rtype : Iter
        :param keyfunc:
        :param valfunc:
        :return:
        """

        if not keyfunc:
            keyfunc = lambda e: e

        if not valfunc:
            valfunc = lambda e: e

        def func(iterable, keyfunc_, valfunc_):
            group_by_collection = defaultdict(list)
            for element in iterable:
                (key, value) = (keyfunc_(element), valfunc_(element))
                group_by_collection[key].append(value)
            for k, v in group_by_collection:
                yield (k, v)
        return Iter(func(self._iter, keyfunc, valfunc))

    def reduce(self, reducing_function, initial=None):
        """
        Get a merged value using an associative reduce function,
        so as to reduce the iterable to a single value from left to right.

        :param reducing_function:
        :param initial:
        :return:
        """
        return reduce(reducing_function, self._iter, initial=initial)

    def reduce_by_key(self, reducing_function, keyfunc=lambda (k, _): k,
                      valfunc=lambda (_, v): v, initial=None):
        """
        Make an iterator that returns the merged values for each key using an associative reduce function.
        The default key and values are the (k,v) values of a 2-tuple.

        :rtype: Iter
        :param reducing_function:
        :param keyfunc:
        :param valfunc:
        :param initial:
        :return:
        """
        return self.groupby(keyfunc, valfunc)\
                   .map(lambda (k, v):
                       (k, reduce(reducing_function, v, initial)))

    def union(self, *iterable):
        """
        Make an iterator that returns elements from the first iterable until it
        is exhausted, then proceeds to the next iterable, until all of the iterables
        are exhausted. Used for treating consecutive sequences as a single sequence.

        :rtype Iter:
        :param iterable:
        :return:
        """
        return Iter(it.chain(self._iter, *iterable))

    def chain(self, iterable):
        """Make an iterator that returns elements from the first iterable until it
        is exhausted, then proceeds to the next iterable, until all of the iterables
        are exhausted. Used for treating consecutive sequences as a single sequence.

        :type iterable: Iterable
        :rtype : Iter
        :param iterable:
        :return:
        """
        return self.union(self, iterable)

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
        Make an iterator with only the distinct elements of the previous.

        :rtype : Iter
        :return:
        """

        def func(iterable):
            # This iterator simply puts elements into a set and looks for
            # simple set membership. Bloom filter implementation may be of interest
            set_of_distinct_values = set()
            for i in iterable:
                if i not in set_of_distinct_values:
                    set_of_distinct_values.add(i)
                    yield i
        return Iter(func(self._iter))

    def distinct_approx(self, init_cap=200, err_rate=0.001):
        """
        Make an iterator with only the distinct elements of the previous.
        Uses a Bloom filter for better space efficiency at the cost of false positive

        :return:
        """
        from pybloom import ScalableBloomFilter

        def func(iterable):
            # This iterator uses a Bloom filter to check for uniqueness, much more memory efficient
            set_of_distinct_values = ScalableBloomFilter(init_cap, err_rate)
            for element in iterable:
                if element not in set_of_distinct_values:
                    set_of_distinct_values.add(element)
                    yield element
        return Iter(func(self._iter))

    def collect(self):
        """
        Collect the iterable back into a list.

        :rtype : list
        :return:
        """
        return list(self._iter)

    def copy_current_state(self):
        """
        Clone the iterable to produce a deepcopy. This may be desired if we wish
        to maintain the state of the iterator while also calling a method with side effects.

        :rtype : Iter
        :return:
        """
        return deepcopy(self);

    def __iter__(self):
        return self._iter
