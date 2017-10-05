from google.appengine.ext import ndb

class Room(ndb.Model):
    su = ndb.StringProperty()
    mo = ndb.StringProperty()
    tu = ndb.StringProperty()
    we = ndb.StringProperty()
    th = ndb.StringProperty()
    fr = ndb.StringProperty()
    sa = ndb.StringProperty()
    last_active = ndb.IntegerProperty()

def get(filter=None, keys_only=False):
    query = Room.query()
    if filter:
        query.filter(filter.split(" "))
    return query.fetch(keys_only=keys_only)

def reset():
    entries = get(keys_only=True)
    ndb.delete_multi(entries)
