from websoc.fetch import iter_websoc
from websoc.parse import parse_document
import antndb

def scrape(years=[], terms=[]):
    'Add schedules of specified or current yearterms to the database.'
    if len(years) > 0:
        if len(terms) > 0:
            yeartermdocs = iter_websoc(years, terms, only_now=False)
        else:
            yeartermdocs = iter_websoc(years, only_now=False)
    else:
        yeartermdocs = iter_websoc()
    keys = antndb.get()

    database = {}
    for yearterm, document in yeartermdocs:
        parse_document(database, document, yearterm)

    for building in database:
        for room in database[building]:
            id = ' '.join([building, room])
            schedule = [
                list(database[building][room]['su']),
                list(database[building][room]['m']),
                list(database[building][room]['tu']),
                list(database[building][room]['w']),
                list(database[building][room]['th']),
                list(database[building][room]['f']),
                list(database[building][room]['sa'])
            ]
            yearterm = database[building][room]['yearterm']
            key = antndb.set(id, building, room, schedule, yearterm)
            if key in keys:
                keys.remove(key)

    antndb.reset_multi(keys)

if __name__ == '__main__':
    scrape()
