import re
from datetime import datetime

timeplacepattern = re.compile('((?:Su|M|Tu|W|Th|F|Sa)+\s*\d+:\d+-\s*\d+:\d+p?)\s+(\w+\s+\w+)')

def parse_document(database, document, yearterm):
    'Extract room data from a websoc document.'
    t = get_timeplace_index(document)
    for block in iter_block(document):
        for line in iter_line(block):
            timeplaces = re.findall(timeplacepattern, line[t:])
            if len(timeplaces) < 1:
                continue
            elif len(timeplaces) > 1:
                print('Warning: Multiple timeplace strings encountered.', timeplace)
            time = timeplaces[0][0]
            place = timeplaces[0][1]
            if '*TBA*' in time or '*TBA*' in place: # remnant of old get_timeplace_indices
                continue
            days, hours = parse_time(time)
            building, room = parse_place(place)
            database.setdefault(building, {})
            database[building].setdefault(room, {
                'su': set(),
                'm': set(),
                'tu': set(),
                'w': set(),
                'th': set(),
                'f': set(),
                'sa': set(),
                'yearterm': yearterm
            })
            for day in days:
                database[building][room][day].add(hours)
    return database

def get_timeplace_index(document):
    'Find the index of Time and Place on a line.'
    lines = document.split('\n')
    for line in lines:
        if 'Time' in line and 'Place' in line and 'Max' in line:
            return line.index('Time')
    return -1

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
    timelow = time.lower()
    days = re.findall('(su|m|tu|w|th|f|sa)', timelow)
    start, end = re.findall('(\d+):(\d+)', timelow)
    hour0 = int(start[0]) + int(start[1]) / 60.0
    hour1 = int(end[0]) + (int(end[1]) + 10) / 60.0 # pad end with 10 minutes
    hours = [hour0, hour1]
    if 'p' in timelow:
        if hours[1] < 12:
            if hours[0] < hours[1]:
                hours[0] += 12
            hours[1] += 12
    return days, tuple(hours)

def parse_place(place):
    'Extract building and room from a websoc place string.'
    buildingroom = place.lower().strip().split()
    while len(buildingroom) < 2:
        buildingroom.append('null')
    return buildingroom[:2]

if __name__ == '__main__':
    import test_websoc_parse
    database = {}
    for d in test_websoc_parse.data:
        parse_document(database, d)
    for d in database:
        print(d, database[d])
