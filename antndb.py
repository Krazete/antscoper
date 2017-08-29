from google.appengine.ext import ndb
from ast import literal_eval

class Room(ndb.Model):
    su = ndb.StringProperty()
    m = ndb.StringProperty()
    tu = ndb.StringProperty()
    w = ndb.StringProperty()
    th = ndb.StringProperty()
    f = ndb.StringProperty()
    sa = ndb.StringProperty()

def get():
    return Room.query().fetch()

def get_keys():
    return Room.query().fetch(keys_only=True)



def reset():
    entries = Room.query().fetch(keys_only=True)
    ndb.delete_multi(entries)
