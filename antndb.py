from google.appengine.ext import ndb

class Schedule(ndb.Model):
    building = ndb.StringProperty()
    room = ndb.StringProperty()

    sunday = ndb.JsonProperty()
    monday = ndb.JsonProperty()
    tuesday = ndb.JsonProperty()
    wednesday = ndb.JsonProperty()
    thursday = ndb.JsonProperty()
    friday = ndb.JsonProperty()
    saturday = ndb.JsonProperty()

def get(filter=None, keys_only=False):
    query = Schedule.query()
    if filter:
        query.filter(filter.split(" "))
    return query.fetch(keys_only=keys_only)

def reset():
    entries = get(keys_only=True)
    ndb.delete_multi(entries)

def get_near():
    pass

def get_next_100():
    pass
