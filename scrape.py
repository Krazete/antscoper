import websoc
import websoc_parse
import antndb

def scrape(year=None, term=None):
    if year:
        data = websoc.get_data(year, term)
        keys = None
    else:
        year = websoc.CURRENT_YEAR
        data = websoc.get_data()
        keys = antndb.get(keys_only=True)

    database = {}
    for document in data:
        websoc_parse.parse_document(database, document)

    for bldg in database:
        for room in database[bldg]:
            entity = antndb.Room(
                id=' '.join([bldg, room]),
                su=str(database[bldg][room]['Su']),
                mo=str(database[bldg][room]['M']),
                tu=str(database[bldg][room]['Tu']),
                we=str(database[bldg][room]['W']),
                th=str(database[bldg][room]['Th']),
                fr=str(database[bldg][room]['F']),
                sa=str(database[bldg][room]['Sa']),
                last_active=year
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
