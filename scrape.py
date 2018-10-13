import websoc
import antndb

def scrape(years=[], terms=[]):
    if len(years) > 0:
        if len(terms) > 0:
            documents = websoc.iter_websoc(years, terms, only_now=False)
        else:
            documents = websoc.iter_websoc(years, only_now=False)
        keys = antndb.get(keys_only=True)
    else:
        documents = websoc.iter_websoc()
        keys = None

    database = {}
    for document in documents:
        websoc.parse_document(database, document)

    for building in database:
        b = antndb.Building(
            name=building,
        )

        for room in database[building]:
            entity = antndb.Room(
                id=' '.join([building, room]),
                sunday=database[building][room]['Su'],
                monday=database[building][room]['M'],
                tuesday=database[building][room]['Tu'],
                wednesday=database[building][room]['W'],
                thursday=database[building][room]['Th'],
                friday=database[building][room]['F'],
                saturday=database[building][room]['Sa'],
                initial_yearterm=''.format(year),
                final_yearterm=''.format(year)
            )
            key = entity.put()
            if keys:
                if key in keys:
                    keys.remove(key)

    if keys:
        entities = antndb.ndb.get_multi(keys)
        for entity in entities:
            entity.su = entity.mo = entity.tu = entity.we = entity.th = entity.fr = entity.sa = '[]'
        antndb.ndb.put_multi(entities)

if __name__ == '__main__':
    scrape()
