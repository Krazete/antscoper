import webapp2
import websoc

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        content = websoc.main()
        self.response.write(content)

class Blah(webapp2.RequestHandler):
    def get(self, path):
        self.response.headers['Content-Type'] = 'text/' + path.split('.')[-1]
        self.response.write(open(path).read())

sitemap = [
    ('/', Index),
    ('/(.*)', Blah)
]

app = webapp2.WSGIApplication(sitemap, debug=True)

import scrape
