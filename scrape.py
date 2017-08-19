from google.appengine.api import datastore
import websoc
import websoc_parse

data = websoc.get_data()

database = {}
for document in data:
    websoc_parse.parse_document(database, document)

for bldg in database:
    for room in database[bldg]:
        entity = datastore.Entity('Room', name=' '.join([bldg, room]))
        for day in database[bldg][room]:
            entity[day] = [str(t) for t in database[bldg][room][day]]
        key = datastore.Put(entity)
        # print key
        # print datastore.Get(key)
        # datastore.Delete(key)
