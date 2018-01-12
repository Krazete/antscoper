from chrono import chronolist
import re

def get_timeplace_indices(document):
    lines = document.split('\n')
    for line in lines:
        if 'CCode' in line and 'Time' in line and 'Place' in line and 'Max' in line:
            t = line.index('Time')
            p = line.index('Place')
            m = line.index('Max')
            return t, p, m

def iterblock(document):
    'Generate each block of the document containing courses.'
    start = document.index('###')
    end = document.index('***')
    blocks = re.split('\n\n+', document[start:end])
    for block in blocks:
        if '###' not in block and '___' not in block:
            yield block

def iterline(block):
    'Generate each line of the block containing schedules.'
    lines = block.split('\n')
    for line in lines[2:]:
        if ' ~ ' not in line:
            yield line

def parse_time(time):
    days = re.findall('(Su|M|Tu|W|Th|F|Sa)', time)
    start, end = re.findall('(\d+):(\d+)', time)
    hours = [int(start[0]) + int(start[1]) / 60.0, int(end[0]) + (int(end[1]) + 10) / 60.0] # TODO: get rid of the +10 buffer remover (requires front-end update too)
    if 'p' in time:
        if hours[1] < 12:
            if hours[0] < hours[1]:
                hours[0] += 12
            hours[1] += 12
    return days, hours

def parse_place(place):
    return place.strip().split(' ', 1)

def parse_document(database, document):
    t, p, m = get_timeplace_indices(document)
    for block in iterblock(document):
        for line in iterline(block):
            time = line[t:p]
            place = line[p:m]
            if 'TBA' in time or 'TBA' in place: # TODO: change with more specific term, '*TBA*'
                continue
            if time.strip() == '' or place.strip == '':
                continue
            days, hours = parse_time(time)
            building, room = parse_place(place)
            database.setdefault(building, {})
            database[building].setdefault(room, {
                'Su': chronolist(),
                'M': chronolist(),
                'Tu': chronolist(),
                'W': chronolist(),
                'Th': chronolist(),
                'F': chronolist(),
                'Sa': chronolist()
            })
            for day in days:
                database[building][room][day].add(hours)
    return database

if __name__ == '__main__':
    import test_websoc_parse
    database = {}
    for d in test_websoc_parse.data:
        parse_document(database, d)
    for d in database:
        print d, database[d]
