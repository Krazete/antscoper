from google.appengine.api import urlfetch
from datetime import datetime

urlfetch.set_default_fetch_deadline(60)

YEARS = range(1990, datetime.now().year + 1)
TERMS = [03, 14, 25, 39, 76, 92] # [Winter, Spring, Summer Session 1, 10-Wk Summer, Summer Session 2, Fall]

def post(yearterm, coursecodes=None):
    'Post a request to WebSoc and return the response.'
    url = 'https://www.reg.uci.edu/perl/WebSoc?YearTerm={}'.format(yearterm) # TODO: maybe change back from format to concatenation
    if coursecodes:
        url += '&Submit=Text&CourseCodes={}'.format(coursecodes)
    return urlfetch.fetch(url).content

def iteryearterm(year=None, term=None):
    'Generate specified or current yearterms.'
    formatyearterm = lambda year, term: '{}-{}'.format(year, str(term).zfill(2))
    if year:
        if term:
            yearterm = formatyearterm(year, term)
            if year == YEARS[-1]:
                if 'Whoa pardner' in post(yearterm):
                    raise StopIteration
            yield yearterm
        else:
            for term in TERMS:
                yearterm = formatyearterm(year, term)
                if year == YEARS[-1]:
                    if 'Whoa pardner' in post(yearterm):
                        raise StopIteration
                yield yearterm
    else:
        for term in TERMS:
            yearterm = formatyearterm(YEARS[-1], term)
            if 'Currently in week' in post(yearterm): # TODO: check if last few weeks are different
                yield yearterm

def itercoursecodes(blocksize=800):
    'Generate coursecodes 0-99999 in blocks of specified size.'
    numblocks = 100000 // blocksize
    remainder = 100000 % blocksize
    for i in range(numblocks):
        a = i * blocksize
        b = a + blocksize - 1
        yield '{}-{}'.format(a, b)
    if remainder > 1:
        a = b + 1
        b = a + remainder - 1
        yield '{}-{}'.format(a, b)

def iterwebsoc(year=None, term=None, blocksize=800):
    'Generate raw data of course schedules from WebSoc.'
    for yearterm in iteryearterm(year, term):
        for coursecodes in itercoursecodes(blocksize):
            content = post(yearterm, coursecodes)
            if 'No courses matched' not in content:
                yield content
