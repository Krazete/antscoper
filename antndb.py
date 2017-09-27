from google.appengine.ext import ndb
from ast import literal_eval

class Room(ndb.Model):
    su = ndb.StringProperty()
    mo = ndb.StringProperty()
    tu = ndb.StringProperty()
    we = ndb.StringProperty()
    th = ndb.StringProperty()
    fr = ndb.StringProperty()
    sa = ndb.StringProperty()

def get():
    return Room.query().fetch()

def get_keys():
    return Room.query().fetch(keys_only=True)

def reset():
    entries = get_keys()
    ndb.delete_multi(entries)
