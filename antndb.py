from google.appengine.ext import ndb

class Schedule(ndb.Model):
    building = ndb.StringProperty()
    room = ndb.StringProperty()

    su = ndb.JsonProperty()
    mo = ndb.JsonProperty()
    tu = ndb.JsonProperty()
    we = ndb.JsonProperty()
    th = ndb.JsonProperty()
    fr = ndb.JsonProperty()
    sa = ndb.JsonProperty()

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
