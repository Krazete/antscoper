class chronolist:
    def __init__(self, l=[]):
        self.list = []
        for e in l:
            self.add(e)
    def __iter__(self):
        return iter(self.list)
    def __len__(self, other):
        return len(self.list)
    def __repr__(self):
        return repr(self.list)
    def __str__(self):
        return str(self.list)
#     def index(self, o):
#         if isinstance(o, (int, float, long, complex)):
#             o = [o, o]
#         for i, e in enumerate(self.list):
#             if e[0] <= o[0] <= o[1] <= e[1]:
#                 return i
#         return -1
    def add(self, o):
        assert len(o) == 2, '{} is not a range'.format(o)
        assert o[0] <= o[1], '{} is not a proper range'.format(o)
        # sorted insert
        i = 0
        for e in self.list:
            if o < e:
                break
            i += 1
        self.list.insert(i, o)
        if len(self.list) == 1:
            return
        # merge remaining
        cutlist = []
        if i >= 1:
            e = self.list[i - 1]
            if o[0] <= e[1]: # check behind
                self.list[i][0] = min(e[0], o[0])
                cutlist.append(e)
        for e in self.list[i + 1:]: # check in front
            if e[0] <= o[1]:
                self.list[i][1] = max(e[1], o[1])
                cutlist.append(e)
            else:
                break
        for e in cutlist:
            self.list.remove(e)
    def remove(self, o):
        assert len(o) == 2, '{} is not a range'.format(o)
        assert o[0] < o[1], '{} is not a proper range'.format(o)
        cutlist = []
        for i, e in enumerate(self.list):
            if o[0] <= e[0] <= o[1] <= e[1]: # o <= e
                self.list[i][0] = o[1]
            if e[0] <= o[0] <= e[1] <= o[1]: # e <= o
                self.list[i][1] = o[0]
            if e[0] <= o[0] <= o[1] <= e[1]: # e surrounds o
                self.list.insert(i, [e[0], o[0]])
                self.list[i + 1][0] = o[0]
            if o[0] <= e[0] <= e[1] <= o[1]: # o surrounds e
                cutlist.append(e)
        for e in cutlist:
            self.list.remove(e)
