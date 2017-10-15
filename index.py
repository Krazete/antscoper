import webapp2
import antndb
from ast import literal_eval
import json
from scrape import scrape
import urllib

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        database = [
            {
                "id": e.key.id(),
                "0": e.su,
                "1": e.mo,
                "2": e.tu,
                "3": e.we,
                "4": e.th,
                "5": e.fr,
                "6": e.sa,
                "last_active": e.last_active
            } for e in antndb.get()
        ]
        self.response.write(open('index.html').read().replace('{WEBSOC_DATA}', json.dumps(database)).replace('{MAP_DATA}', urllib.urlopen('https://map.uci.edu/map/api/v2/locations?map=463&api_key=3715298bef4e8732196adf0b95254dd5').read()))

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
