import websoc
import antndb

def scrape(years=[], terms=[]):
    'Add schedules of specified or current yearterms to the database.'
    if len(years) > 0:
        if len(terms) > 0:
            documents = websoc.iter_websoc(years, terms, only_now=False)
        else:
            documents = websoc.iter_websoc(years, only_now=False)
        keys = antndb.get()
    else:
        documents = websoc.iter_websoc()
        keys = []

    database = {}
    for document in documents:
        websoc.parse_document(database, document)

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
            datestamp = database[building][room]['datestamp']
            key = antndb.set(id, building, room, schedule, datestamp)
            if key in keys:
                keys.remove(key)

    antndb.reset_multi(keys)

if __name__ == '__main__':
    scrape()
