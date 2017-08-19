import webapp2

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(open('index.html').read())

class Other(webapp2.RequestHandler):
    def get(self, path):
        self.response.headers['Content-Type'] = 'text/' + path.split('.')[-1] # greedy
        self.response.write(open(path).read())

sitemap = [
    ('/', Index),
    ('/(.*)', Other)
]

app = webapp2.WSGIApplication(sitemap, debug=True)
