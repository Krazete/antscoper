from scrape import scrape
import webapp2

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(open('index.html').read().replace('{WEBSOC_DATA}', '999999999'))

class Scrape(webapp2.RequestHandler):
    def post(self):
        year = int(self.request.get('year', None))
        self.response.write(year)
        scrape(year)
        self.response.write(' has been added to the database.')

sitemap = [
    ('/', Index),
    ('/scrape', Scrape)
]

app = webapp2.WSGIApplication(sitemap, debug=True)
