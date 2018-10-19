from google.appengine.ext import ndb

class Schedule(ndb.Model):
    building = ndb.StringProperty()
    room = ndb.StringProperty()
    schedule = ndb.JsonProperty()
    datestamp = ndb.DateProperty()

def get(filter=None, keys_only=True):
    'Get a list of specific entities or their keys.'
    query = Schedule.query()
    if filter:
        query = query.filter(ndb.query.FilterNode(filter.split(' ')))
    return query.fetch(keys_only=keys_only)

def set(id, building, room, schedule, datestamp):
    'Add or change an entity in the Schedule model.'
    entity = Schedule(
        id=id, building=building, room=room,
        schedule=schedule, datestamp=datestamp
    )
    key = entity.put()
    return key

def reset_multi(keys):
    'Clear the schedule of a list of entities specified by key.'
    entities = ndb.get_multi(keys)
    for entity in entities:
        entity.schedule = [[],[],[],[],[],[],[]]
    ndb.put_multi(entities)

def delete_all():
    'Delete the Schedule and all of its entities.'
    entries = get()
    ndb.delete_multi(entries)
