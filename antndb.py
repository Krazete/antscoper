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

    initial_date = ndb.DateProperty()
    final_date = ndb.DateProperty()

def get(filter=None, keys_only=True):
    'Get a list of specific entities or their keys.'
    query = Schedule.query()
    if filter:
        query.filter(filter.split(' '))
    return query.fetch(keys_only=keys_only)

def set(id, building, room, su, mo, tu, we, th, fr, sa, datestamp):
    'Add or change an entity in the Schedule model.'
    initial_date = final_date = datestamp
    for schedule in get(keys_only=False):
        if id == schedule.key.id():
            initial_date = min(schedule.initial_date, datestamp)
            final_date = max(datestamp, schedule.final_date)
    entity = Schedule(
        id=id, building=building, room=room,
        su=su, mo=mo, tu=tu, we=we, th=th, fr=fr, sa=sa,
        initial_date=initial_date, final_date=final_date
    )
    key = entity.put()
    return key

def reset_multi(keys):
    'Clear the schedule of a list of entities specified by key.'
    entities = ndb.get_multi(keys)
    for entity in entities:
        entity.su = entity.mo = entity.tu = entity.we = entity.th = entity.fr = entity.sa = '[]'
    ndb.put_multi(entities)

def delete_all():
    'Delete the Schedule and all of its entities.'
    entries = get()
    ndb.delete_multi(entries)
