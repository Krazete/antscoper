from google.appengine.ext import ndb

class Room(ndb.Model):
    su = ndb.JsonProperty()
    mo = ndb.JsonProperty()
    tu = ndb.JsonProperty()
    we = ndb.JsonProperty()
    th = ndb.JsonProperty()
    fr = ndb.JsonProperty()
    sa = ndb.JsonProperty()
    last_active = ndb.IntegerProperty()

def get(filter=None, keys_only=False):
    query = Room.query()
    if filter:
        query.filter(filter.split(" "))
    return query.fetch(keys_only=keys_only)

def reset():
    entries = get(keys_only=True)
    ndb.delete_multi(entries)
