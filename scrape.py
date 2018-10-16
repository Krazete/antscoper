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
                su=list(database[building][room]['su']),
                mo=list(database[building][room]['m']),
                tu=list(database[building][room]['tu']),
                we=list(database[building][room]['w']),
                th=list(database[building][room]['th']),
                fr=list(database[building][room]['f']),
                sa=list(database[building][room]['sa'])
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
