import re
from datetime import datetime

def parse_document(database, document, yearterm):
    'Extract room data from a websoc document.'
    t, p, m = get_timeplace_indices(document)
    for block in iter_block(document):
        for line in iter_line(block):
            time = line[t:p]
            place = line[p:m]
            if '*TBA*' in time or '*TBA*' in place:
                continue
            if time.strip() == '' or place.strip() == '':
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
    buildingroom = place.lower().strip().split(None, 1)
    while len(buildingroom) < 2:
        buildingroom.append('null')
    return buildingroom

if __name__ == '__main__':
    import test_websoc_parse
    database = {}
    for d in test_websoc_parse.data:
        parse_document(database, d)
    for d in database:
        print d, database[d]
