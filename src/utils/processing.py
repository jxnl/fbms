class ListMapDict(object):
    """Consume a list of functions and apply every function onto an element
    to produce a dict that maps the feature to the value

    attributes:
        fl (listof functions) - feature producing functions
        labels (listof str) - names of features
    """
    def __init__(self, funcList, labels=None):
        self.fl = funcList
        if labels:
            self.lb = labels
        else:
            self.lb = (f.__name__ for f in funcList)

    def apply(self, data):
        output = dict()
        for (l, f) in zip(self.lbl, self.fl):
            output[l] = f(data)
        return output
