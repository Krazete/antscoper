from google.appengine.ext import ndb

class Room(ndb.Model):
    building = ndb.StringProperty()
    room = ndb.StringProperty()

    sunday = ndb.JsonProperty()
    monday = ndb.JsonProperty()
    tuesday = ndb.JsonProperty()
    wednesday = ndb.JsonProperty()
    thursday = ndb.JsonProperty()
    friday = ndb.JsonProperty()
    saturday = ndb.JsonProperty()

    initial_yearterm = ndb.StringProperty()
    final_yearterm = ndb.StringProperty()

class Building(ndb.Model):
    name = ndb.StringProperty()
    initials = ndb.StringProperty()

    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    distance = ndb.ComputedProperty(lambda x, y: ((latitude - x)**2 + (longitude - y)**2) ** 0.5) # google this and change to world-distance formula

    rooms = ndb.StructuredProperty(Room, repeated=True)

def get(filter=None, keys_only=False):
    query = Room.query()
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
