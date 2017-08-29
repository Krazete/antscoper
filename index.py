import webapp2
import antndb

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(open('index.html').read().replace('{WEBSOC_DATA}', '999999999'))
        self.response.write('<div>' + str(antndb.get()) + '</div>')

sitemap = [('/', Index)]

app = webapp2.WSGIApplication(sitemap, debug=True)
