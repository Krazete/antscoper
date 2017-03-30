import webapp2
import websoc

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        content = websoc.main()
        
        self.response.write(content)

sitemap = [
    ('/', Index)
]

app = webapp2.WSGIApplication(sitemap, debug = True)
