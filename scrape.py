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
                sunday=database[bldg][room]['Su'].list,
                monday=database[bldg][room]['M'].list,
                tuesday=database[bldg][room]['Tu'].list,
                wednesday=database[bldg][room]['W'].list,
                thursday=database[bldg][room]['Th'].list,
                friday=database[bldg][room]['F'].list,
                saturday=database[bldg][room]['Sa'].list,
                initial_term=year
                final_term=year
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
