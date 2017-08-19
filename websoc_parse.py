from chrono import chronolist as CL
import re

def get_timeplace_indices(document):
    lines = document.split('\n')
    for line in lines:
        if 'CCode' in line:
            i = line.index('Time')
            j = line.index('Place')
            k = line.index('Max')
            return i, j, k

def document2blocks(document):
    start = document.index('###')
    end = document.index('***')
    all_blocks = re.split('\n\n+', document[start:end])
    blocks = filter(lambda b: '###' not in b and '___' not in b, all_blocks)
    return blocks

def block2lines(block):
    all_lines = block.split('\n')
    lines = filter(lambda l: ' ~ ' not in l, all_lines[2:])
    return lines

def parse_document(database, document):
    i, j, k = get_timeplace_indices(document)
    blocks = document2blocks(document)
    for block in blocks:
        lines = block2lines(block)
        for line in lines:
            # print line # debugging
            time = line[i:j]
            place = line[j:k]
            timeplace = time + place
            if 'TBA' not in timeplace and timeplace.strip() != '':
                days, hours = parse_time(time)
                building, room = parse_place(place)
                if building not in database:
                    database.setdefault(building, {})
                if room not in database[building]:
                    database[building].setdefault(room, {'Su': CL(), 'M': CL(), 'Tu': CL(), 'W': CL(), 'Th': CL(), 'F': CL(), 'Sa': CL()})
                for day in days:
                    database[building][room][day].add(hours)
    return database

def parse_time(time):
    days = re.findall('(Su|M|Tu|W|Th|F|Sa)', time)
    start, end = re.findall('(\d+):(\d+)(.)', time)
    hours = [int(start[0]) + int(start[1]) / 60, int(end[0]) + (int(end[1]) + 10) / 60]
    if 'p' in time:
        if hours[1] < 12:
            if hours[0] < hours[1]:
                hours[0] += 12
            hours[1] += 12
    return days, hours

def parse_place(place):
    return place.strip().split(' ')

if __name__ == '__main__':
    import test
    database = {}
    for d in test.data:
        parse_document(database, d)
    for d in database:
        print d, database[d]
