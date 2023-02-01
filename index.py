import json
import urllib
import traceback
import antndb
from flask import Flask, Response, request
from scrape import scrape
from websoc import YEAR_NOW

app = Flask(__name__)

@app.route('/')
def index_get():
    contenttype = 'text/html'
    content = open('index.html').read()
    return Response(content, mimetype=contenttype)

@app.route('/map.json')
def map_get():
    contenttype = 'application/json'
    mapurl = 'https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5'
    # https://map.uci.edu/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5
    # https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5
    # http://map.concept3d.com/?id=463
    # https://www.reg.uci.edu/perl/WebSoc?YearTerm=1990-03&CourseCodes=0-99999&Submit=Text
    try:
        mapjson = urllib.request.urlopen(mapurl).read()
        if len(mapjson) <= 0:
            raise
    except:
        mapjson = open('geo_backup.json').read()
    return Response(mapjson, mimetype=contenttype)

@app.route('/data.json')
def data_get():
    contenttype = 'application/json'
    try:
        database = {}
        for schedule in antndb.Schedule.query().fetch():
            year = int(schedule.yearterm.split('-')[0])
            if year >= YEAR_NOW - 1: # show this year and last year only
                building = schedule.building
                room = schedule.room
                database.setdefault(building, {})
                database[building].setdefault(room, {
                    'schedule': schedule.schedule,
                    'yearterm': schedule.yearterm
                })
        datajson = json.dumps(database)
    except:
        datajson = open('database_backup.json').read()
    return Response(datajson, mimetype=contenttype)

@app.post('/data.json')
def data_post():
    building = request.get('building', 'alh')
    database = {}
    try:
        query = antndb.Schedule.query().filter(antndb.ndb.StringProperty('building') == building)
        for schedule in query.fetch():
            year = int(schedule.yearterm.split('-')[0])
            if year >= YEAR_NOW - 1: # show this year and last year only
                building = schedule.building
                room = schedule.room
                database.setdefault(building, {})
                database[building].setdefault(room, {
                    'schedule': schedule.schedule,
                    'yearterm': schedule.yearterm
                })
    except:
        database.setdefault('error', {
            'over': {
                'schedule': [[],[],[],[],[],[],[]],
                'yearterm': '0000-00'
            },
            'quota': {
                'schedule': [[],[],[],[],[],[],[]],
                'yearterm': '0000-00'
            }
        })
    datajson = json.dumps(database)
    return Response(datajson, mimetype=contenttype)

@app.route('/scrape_yearterm')
def scrape_yearterm_get():
    contenttype = 'text/html'
    template = open('scrape_yearterm.html').read()
    content = template.replace('{YEAR_VALUE}', '1990').replace('{INPUT_INDEX}', '1')
    return Response(content, mimetype=contenttype)

@app.post('/scrape_yearterm')
def scrape_yearterm_post():
    year = int(request.get('year', 1990))
    term = int(request.get('term', 92))
    template = open('scrape_yearterm.html').read()
    try:
        scrape([year], [term])
        content = 'YearTerm {:04d}-{:02d} has successfully been added to the database.<br><br>'.format(year, term)
        year_value = str(year + 1 if term == 92 else year) # iterate year
        input_index = str([0, 92, 03, 14, 25, 39, 76].index(term)) # iterate term
    except Exception as e:
        traceback.print_exc() # only visible in terminal
        content = 'ERROR: {}<br><br>'.format(e)
        year_value = str(year) # preserve year
        input_index = str([0, 03, 14, 25, 39, 76, 92].index(term)) # preserve term
    content += template.replace('{YEAR_VALUE}', year_value).replace('{INPUT_INDEX}', input_index)
    return Response(content, mimetype=contenttype)
