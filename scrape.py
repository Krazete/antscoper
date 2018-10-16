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
        for room in database[building]:
            entity = antndb.Schedule(
                id=' '.join([building, room]),
                building=building,
                room=room,
                sunday=list(database[building][room]['Su']),
                monday=list(database[building][room]['M']),
                tuesday=list(database[building][room]['Tu']),
                wednesday=list(database[building][room]['W']),
                thursday=list(database[building][room]['Th']),
                friday=list(database[building][room]['F']),
                saturday=list(database[building][room]['Sa'])
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
