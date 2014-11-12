import itertools as it


class Iter(object):

    def __init__(self, iterable):
        self._iter = iterable

    def map(self, f):
        return Iter(it.imap(f, (self._iter)))

    def flatmap(self, f):
        return Iter(it.chain(self.map(f)._iter))

    def filter(self, f):
        return Iter(it.ifilter(f, (self._iter)))

    def filterfalse(self, f):
        return Iter(it.ifilterfalse(f, (self._iter)))

    def takewhile(self, f):
        return Iter(it.takewhile(f, (self._iter)))

    def dropwhile(self, f):
        return Iter(it.dropwhile(f, (self._iter)))

    def groupby(self, f):
        return Iter(it.groupby(f, (self._iter)))

    def chain(self, seq):
        return Iter(it.chain(seq, (self._iter)))

    def slice(self, *args):
        return Iter(it.islice((self._iter), *args))

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
