import itertools


class Iter(object):

    def __init__(self, iterable):
        self._iter = iterable

    def map(self, f):
        return Iter(itertools.imap(f, (self._iter)))

    def flatmap(self, f):
        return Iter(itertools.chain(self.map(f)._iter))

    def filter(self, f):
        return Iter(itertools.ifilter(f, (self._iter)))

    def filterfalse(self, f):
        return Iter(itertools.ifilterfalse(f, (self._iter)))

    def takewhile(self, f):
        return Iter(itertools.takewhile(f, (self._iter)))

    def dropwhile(self, f):
        return Iter(itertools.dropwhile(f, (self._iter)))

    def groupby(self, f):
        return Iter(itertools.groupby(f, (self._iter)))

    def chain(self, seq):
        return Iter(itertools.chain(seq, (self._iter)))

    def slice(self, *args):
        return Iter(itertools.islice((self._iter), *args))

    def take(self, max):
        def func(iterable):
            for i, e in enumerate(iterable):
                if i < max:
                    yield e
        return Iter(func(self._iter))

    def __str__(self):
        return str(list(self._iter))

    def __iter__(self):
        return self._iter
