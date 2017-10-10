class chronolist:
    def __init__(self, items=[]):
        self.list = []
        for item in items:
            self.add(item)
    def __iter__(self):
        return iter(self.list)
    def __len__(self, other):
        return len(self.list)
    def __repr__(self):
        return repr(self.list)
    def __str__(self):
        return str(self.list)
    # def index(self, new_item):
    #     if isinstance(new_item, (int, float, long, complex)):
    #         new_item = [new_item, new_item]
    #     for i, item in enumerate(self.list):
    #         if item[0] <= new_item[0] <= new_item[1] <= item[1]:
    #             return i
    #     return -1
    def add(self, new_item):
        assert len(new_item) == 2, '{} is not a range'.format(o)
        assert new_item[0] <= new_item[1], '{} is not a proper range'.format(o)
        # sorted insert
        i = 0
        for item in self.list:
            if new_item < item:
                break
            i += 1
        self.list.insert(i, new_item)
        if len(self.list) == 1:
            return
        # merge remaining
        cutlist = []
        if i >= 1:
            item = self.list[i - 1]
            if new_item[0] <= item[1]: # check behind
                self.list[i][0] = min(item[0], new_item[0])
                cutlist.append(item)
        for item in self.list[i + 1:]: # check in front
            if item[0] <= new_item[1]:
                self.list[i][1] = max(item[1], new_item[1])
                cutlist.append(item)
            else:
                break
        for item in cutlist:
            self.list.remove(item)
    def remove(self, new_item):
        assert len(new_item) == 2, '{} is not a range'.format(o)
        assert new_item[0] < new_item[1], '{} is not a proper range'.format(o)
        cutlist = []
        for i, item in enumerate(self.list):
            if new_item[0] <= item[0] <= new_item[1] <= item[1]: # new_item <= item
                self.list[i][0] = new_item[1]
            if item[0] <= new_item[0] <= item[1] <= new_item[1]: # item <= new_item
                self.list[i][1] = new_item[0]
            if item[0] <= new_item[0] <= new_item[1] <= item[1]: # item surrounds new_item
                self.list.insert(i, [item[0], new_item[0]])
                self.list[i + 1][0] = new_item[0]
            if new_item[0] <= item[0] <= item[1] <= new_item[1]: # new_item surrounds item
                cutlist.append(item)
        for item in cutlist:
            self.list.remove(item)
