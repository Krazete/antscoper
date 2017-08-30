import websoc
import websoc_parse
import antndb

data = websoc.get_data()

database = {}
for document in data:
    websoc_parse.parse_document(database, document)

keys = antndb.get_keys()

for bldg in database:
    for room in database[bldg]:
        entity = antndb.Room(
            id=' '.join([bldg, room]),
            su=str(database[bldg][room]['Su']),
            m=str(database[bldg][room]['M']),
            tu=str(database[bldg][room]['Tu']),
            w=str(database[bldg][room]['W']),
            th=str(database[bldg][room]['Th']),
            f=str(database[bldg][room]['F']),
            sa=str(database[bldg][room]['Sa'])
        )
        key = entity.put()
        if key in keys:
            keys.remove(key)

entities = ndb.get_multi(keys)
ndb.put_multi(entities)

for key in keys:
    entity = key.get()
    entity.su = entity.m = entity.tu = entity.w = entity.th = entity.f = entity.sa = '[]'
    entity.put()
