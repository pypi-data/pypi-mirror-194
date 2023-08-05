
class NoneValue:

    def __hash__(self):
        return hash(None)

    def __getitem__(self, item):
        if item is Ellipsis:
            return []
        else:
            return none

    def __bool__(self):
        return False

    def __repr__(self):
        return "NoneValue"

    def __str__(self):
        return ""

    def __float__(self):
        return 0.0

    def __int__(self):
        return 0


none = NoneValue()


class List(list):

    def __getitem__(self, item):
        # print(item)
        if item is Ellipsis:
            return self
        else:
            r = super(List, self).__getitem__(item)
            if isinstance(r, dict):
                return Dict(r)
            elif isinstance(r, list):
                return List(r)
            else:
                return r

    def __iter__(self):
        self.start = 0
        return self

    def __next__(self):
        if self.start >= self.__len__():
            raise StopIteration
        r = super(List, self).__getitem__(self.start)
        self.start += 1
        if isinstance(r, dict):
            return Dict(r)
        else:
            return r


class Dict(dict):

    def __getitem__(self, item):
        r = self.get(item)
        if isinstance(r, list):
            return List(r)
        elif r is None:
            return none
        elif isinstance(r, dict):
            return Dict(r)
        else:
            return r
