import webapp2
import antndb
from ast import literal_eval
from json import dumps
from scrape import scrape

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        database = [
            {
                "bldg": e.key.id().split(" ", 1)[0],
                "room": e.key.id().split(" ", 1)[1],
                "su": literal_eval(e.su),
                "mo": literal_eval(e.mo),
                "tu": literal_eval(e.tu),
                "we": literal_eval(e.we),
                "th": literal_eval(e.th),
                "fr": literal_eval(e.fr),
                "sa": literal_eval(e.sa),
                "last_active": e.last_active
            } for e in antndb.get()
        ]
        self.response.write(open('index.html').read().replace('{WEBSOC_DATA}', dumps(database)))

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
