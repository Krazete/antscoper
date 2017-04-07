from google.appengine.api import urlfetch
from datetime import datetime

# https://github.com/gumho/antplanner2/blob/b8501534787b6541f05626907b18bd273e8bc567/antplanner2/views.py
# https://www.reg.uci.edu/perl/WebSoc?YearTerm=2016-92&Submit=TextResults&CourseCodes=50000-54000

'''
javascript:
/* Gets YearTerms from the WebSoc menu. */
console.log(
    ["Fall", "Winter", "Spring", "Session 1", "Session 2", "10-wk", "COM"]
    .map(function(t){
        return Array.from(new Set(
               Array.from(document.forms[1].YearTerm.options)
               .filter(function(e){return e.innerHTML.includes(t)})
               .map(function(e){return e.value.split("-")[1]})
        ))[0]
    })
);

/* Manually loops through CourseCode blocks. */
var yearterm = "2016-92";
var block = 1000;
var next = Number(location.search
           .slice(location.search.lastIndexOf("=") + 1)
           .split("-")[0]) + block;
if(next + block > 100000){
    next = 0;
}
location = "https://www.reg.uci.edu/perl/WebSoc?YearTerm=" + yearterm
         + "&Submit=TextResults&CourseCodes=" + next + "-" + (next + block - 1);

/* Gets all fieldnames from the WebSoc menu. */
Array.from(new Set(
Array.from(document.forms[1].elements)
.map(function(e){return e.name})))
'''

# WEBSOC MAP

class websoc:
    def __init__(self):
        return

def post(yt, cc=None):
    'Requests data from WebSoc and returns the response.'
    url = 'https://www.reg.uci.edu/perl/WebSoc?YearTerm=' + yt
    if cc:
        url += '&Submit=TextResults&CourseCodes=' + cc
    fetched = urlfetch.fetch(url)
    return fetched.content

def yearterms():
    'Generates YearTerms from the current year.'
    y = str(datetime.now().year)
    ts = ['92', '03', '14', '25', '76', '39', '51']
    yts = [y + '-' + t for t in ts]
    for yt in yts:
        data = post(yt)
        if 'Currently in week' in data or 'Instruction starts on' in data:
            yield yt

def coursecodes():
    'Generates CourseCodes from 0 to 99999 in blocks of 2000.'
    for n in range(50):
        a = n * 1000
        b = a + 999
        yield str(a) + '-' + str(b)

def main():
    db = []
    for yt in yearterms():
        for cc in coursecodes():
            data = post(yt, cc)
            if 'No courses matched' not in data:
                db.append(data)
                break # Sample the first 1000.
    return db

def parse(data):
    d = []
    
    lines = data.split('\n')
    for line in lines:
        if line != '':
            d.append(line)

    return d

def update_cache():
    pass
