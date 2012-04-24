class Point(object):
    def __init__(self, file = None, rank = None):
        self.file = file
        self.rank = rank


    def __setattr__(self, key, value):
        if (type(value).__name__ == "str") and (key == "file"):
            self.__dict__[key] = {
                'a': lambda: 1,
                'b': lambda: 2,
                'c': lambda: 3,
                'd': lambda: 4,
                'e': lambda: 5,
                'f': lambda: 6,
                'g': lambda: 7,
                'h': lambda: 8,
                '': lambda : None
                }[value]()
        else:
            self.__dict__[key] = value

    def __cmp__(self, other):
        if (self.file == other.file) and (self.rank == other.rank):
            return 0
        else:
            return 1


