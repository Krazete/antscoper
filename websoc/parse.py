import re

class Chronos:
    def __init__(self, timespans=[]):
        self.times = []
        for timespan in timespans:
            self.insert_timespan(timespan)

    def insert_timespan(self, timespan):
        time_a, time_b = timespan
        a = self.insert_time(time_a)
        b = self.insert_time(time_b)
        self.times = self.times[:a + 1] + self.times[b:]

    def insert_time(self, time):
        i = self.get_index(time)
        self.times = self.times[:i] + [time] + self.times[i:]
        return i

    def get_index(self, new_time):
        for i, time in enumerate(self.times):
            if new_time <= time:
                return i
        return len(self.times)

    def get_timespans(self):
        evens = self.times[0::2]
        odds = self.times[1::2]
        return zip(evens, odds)

    def __iter__(self):
        return iter(self.get_timespans())

    def __repr__(self): # TODO: remove if unnecessary
        return str(self.get_timespans())

def parse_document(database, document):
    'Extract room data from a websoc document.'
    # year = get_year(document)
    t, p, m = get_timeplace_indices(document)
    for block in iter_block(document):
        for line in iter_line(block):
            time = line[t:p]
            place = line[p:m]
            if 'TBA' in time or 'TBA' in place: # TODO: maybe change to '*TBA*'
                continue
            if time.strip() == '' or place.strip() == '':
                continue
            days, hours = parse_time(time)
            building, room = parse_place(place)
            database.setdefault(building, {})
            database[building].setdefault(room, {
                'Su': Chronos(),
                'M': Chronos(),
                'Tu': Chronos(),
                'W': Chronos(),
                'Th': Chronos(),
                'F': Chronos(),
                'Sa': Chronos()
            })
            for day in days:
                database[building][room][day].insert_timespan(hours)
            # database[building][room].setdefault('initial_year', year)
            # database[building][room]['final_year'] = year
    return database

# def get_year(document):
#     'Find the year of the document.'
#     lines = document.split('\n')
#     for line in lines:
#         year = re.match('\d{4}', line)
#         return year
#     return 0

def get_timeplace_indices(document):
    'Find the indices of Time, Place, and Max on a line.'
    lines = document.split('\n')
    for line in lines:
        if 'Time' in line and 'Place' in line and 'Max' in line:
            t = line.index('Time')
            p = line.index('Place')
            m = line.index('Max')
            return t, p, m
    return 0, 0, 0

def iter_block(document):
    'Generate each block of the document containing courses.'
    start = document.index('###')
    end = document.index('***')
    blocks = re.split('\n\n+', document[start:end])
    for block in blocks:
        if '###' not in block and '___' not in block:
            yield block

def iter_line(block):
    'Generate each line of the block containing schedules.'
    lines = block.split('\n')
    for line in lines[2:]:
        if '~' not in line: # '~' marks duplicate courses
            yield line

def parse_time(time):
    'Extract days and hours from a websoc time string.'
    days = re.findall('(Su|M|Tu|W|Th|F|Sa)', time)
    start, end = re.findall('(\d+):(\d+)', time)
    hour0 = int(start[0]) + int(start[1]) / 60.0
    hour1 = int(end[0]) + (int(end[1]) + 10) / 60.0 # TODO: maybe remove +10
    hours = [hour0, hour1]
    if 'p' in time:
        if hours[1] < 12:
            if hours[0] < hours[1]:
                hours[0] += 12
            hours[1] += 12
    return days, hours

def parse_place(place):
    'Extract building and room from a websoc place string.'
    return place.split()

if __name__ == '__main__':
    import test_websoc_parse
    database = {}
    for d in test_websoc_parse.data:
        parse_document(database, d)
    for d in database:
        print d, database[d]
