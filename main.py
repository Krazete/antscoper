import json
import traceback
import antndb
from flask import Flask, Response, request, render_template
from scrape import scrape
from websoc.fetch import YEAR_NOW

app = Flask(__name__)

@app.route('/')
def index_get():
    return render_template('index.html')

@app.route('/data.json')
def data_get():
    try:
        with antndb.client.context():
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
        with antndb.client.context():
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
    form = request.form.to_dict()
    year = int(form.get('year', 1990))
    term = int(form.get('term', 92))
    try:
        scrape([year], [term])
        content = 'YearTerm {:04d}-{:02d} has successfully been added to the database.<br><br>'.format(year, term)
        year_value = year + 1 if term == 92 else year # iterate year
        input_index = [0, 92, 3, 14, 25, 39, 76].index(term) # iterate term
    except Exception as e:
        traceback.print_exc() # only visible in terminal
        content = 'ERROR: {}<br><br>'.format(e)
        year_value = year # preserve year
        input_index = [0, 3, 14, 25, 39, 76, 92].index(term) # preserve term
    template = render_template('scrape_yearterm.html', year_value=year_value, input_index=input_index)
    return content + template

@app.post('/scrape')
def scrape_post():
    try:
        content = scrape()
        return 'SUCCESS: {}'.format(content)
    except Exception as e:
        return 'ERROR: {}'.format(e)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
