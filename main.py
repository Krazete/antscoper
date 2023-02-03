import json
import urllib
import traceback
# import antndb
from flask import Flask, Response, request, render_template
from scrape import scrape
from websoc.fetch import YEAR_NOW

app = Flask(__name__)

@app.route('/')
def index_get():
    return render_template('index.html')

@app.route('/map.json')
def map_get():
    mapurl = 'https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5'
    # Miscellaneous Relevant URLs:
    # - https://map.uci.edu/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5
    # - https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5
    # - http://map.concept3d.com/?id=463
    # - https://www.reg.uci.edu/perl/WebSoc?YearTerm=1990-03&CourseCodes=0-99999&Submit=Text
    try:
        mapjson = urllib.request.urlopen(mapurl).read()
        if len(mapjson) <= 0:
            raise
    except:
        mapjson = open('static/geo_backup.json').read()
    return Response(mapjson, mimetype='application/json')

@app.route('/data.json')
def data_get():
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
        datajson = open('static/database_backup.json').read()
    return Response(datajson, mimetype='application/json')

@app.post('/data.json')
def data_post():
    building = request.args.get('building', 'alh')
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
    return Response(datajson)

@app.route('/scrape_yearterm')
def scrape_yearterm_get():
    return render_template('scrape_yearterm.html', year_value=1990, input_index=1)

@app.post('/scrape_yearterm')
def scrape_yearterm_post():
    year = int(request.args.get('year', 1990))
    term = int(request.args.get('term', 92))
    template = render_template('scrape_yearterm.html')
    try:
        scrape([year], [term])
        content = 'YearTerm {:04d}-{:02d} has successfully been added to the database.<br><br>'.format(year, term)
        year_value = str(year + 1 if term == 92 else year) # iterate year
        input_index = str(['0', '92', '03', '14', '25', '39', '76'].index(str(term))) # iterate term
    except Exception as e:
        traceback.print_exc() # only visible in terminal
        content = 'ERROR: {}<br><br>'.format(e)
        year_value = str(year) # preserve year
        input_index = str(['0', '03', '14', '25', '39', '76', '92'].index(str(term))) # preserve term
    content += template.replace('{YEAR_VALUE}', year_value).replace('{INPUT_INDEX}', input_index)
    return content

@app.post('/scrape')
def scrape_post():
    try:
        scrape()
        return 'Success'
    except Exception as e:
        return 'Error: {}'.format(e)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
