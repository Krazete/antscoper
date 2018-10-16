import webapp2
import antndb
from ast import literal_eval
import json
from scrape import scrape
import urllib

MAPURL = 'https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5'
# https://map.uci.edu/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5
# https://www.myatlascms.com/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5
# http://map.concept3d.com/?id=463

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        database = {}
        for schedule in antndb.Schedule.query().fetch():
            building = schedule.building
            room = schedule.room
            database.setdefault(building, {})
            database[building].setdefault(room, {
                "0": schedule.sunday,
                "1": schedule.monday,
                "2": schedule.tuesday,
                "3": schedule.wednesday,
                "4": schedule.thursday,
                "5": schedule.friday,
                "6": schedule.saturday
            })
        template = open('index.html').read()
        datajson = json.dumps(database)
        mapjson = urllib.urlopen(MAPURL).read()
        content = template.replace('{WEBSOC_DATA}', datajson).replace('{MAP_DATA}', mapjson)
        self.response.write(content)

class Initialize(webapp2.RequestHandler):
    def post(self):
        year = int(self.request.get('year', None))
        term = self.request.get('term', None)
        scrape(year, term)
        self.response.write('{} ({}) has been added to the database.'.format(year, term))

sitemap = [
    ('/', Index),
    ('/initialize_database', Initialize)
]

app = webapp2.WSGIApplication(sitemap, debug=True)
