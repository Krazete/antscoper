from google.appengine.api import urlfetch
from datetime import datetime

urlfetch.set_default_fetch_deadline(60)

YEAR_NOW = datetime.now().year # TODO: set timezone to pst
YEARS = range(1990, YEAR_NOW + 1)
TERMS = [03, 14, 25, 39, 76, 92] # [Winter, Spring, Summer Session 1, 10-Wk Summer, Summer Session 2, Fall]

def iter_websoc(years=[YEAR_NOW], terms=TERMS, blocksize=800, only_now=True):
    'Generate raw data of course schedules from WebSoc.'
    for yearterm in iter_yearterm(years, terms):
        for coursecodes in iter_coursecodes(blocksize):
            document = post(yearterm, coursecodes)
            if 'Whoa pardner' in document or 'No courses matched' in document:
                continue
            if not only_now or 'Currently in week' in document: # TODO: check if last few weeks are different
                yield document

def iter_yearterm(years, terms):
    'Generate specified yearterms.'
    for year in years:
        for term in terms:
            yearterm = '{:04d}-{:02d}'.format(year, term)
            yield yearterm

def iter_coursecodes(blocksize):
    'Generate coursecodes 0-99999 in blocks of specified size.'
    n = 100000 // blocksize
    if 100000 % blocksize > 0:
        n += 1 # basically math.ceil(100000 / blocksize)
    for i in range(n):
        a = i * blocksize
        b = min(a + blocksize - 1, 99999)
        yield '{}-{}'.format(a, b)

def post(yearterm, coursecodes):
    'Post a request to WebSoc and return the response.'
    url = 'https://www.reg.uci.edu/perl/WebSoc'
    query_template = '?YearTerm={}&CourseCodes={}&Submit=Text'
    query = query_template.format(yearterm, coursecodes)
    return urlfetch.fetch(url + query).content
