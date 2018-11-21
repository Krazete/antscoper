from google.appengine.api import urlfetch
from datetime import datetime, timedelta

urlfetch.set_default_fetch_deadline(60)

YEAR_NOW = (datetime.utcnow() + timedelta(hours=-8)).year
YEARS = range(1990, YEAR_NOW + 1)
TERMS = [03, 14, 25, 39, 76, 92]
# [Winter, Spring, Summer Session 1, 10-Wk Summer, Summer Session 2, Fall]

def iter_websoc(years=[YEAR_NOW], terms=TERMS, only_now=True):
    'Generate raw data of course schedules from WebSoc.'
    for yearterm in iter_yearterm(years, terms):
        for document in iter_valid_documents(yearterm):
            if not only_now or 'Currently in week' in document: # TODO: check if last few weeks have a different string
                yield yearterm, document

def iter_yearterm(years, terms):
    'Generate specified yearterms.'
    for year in years:
        for term in terms:
            yearterm = '{:04d}-{:02d}'.format(year, term)
            yield yearterm

def iter_valid_documents(yearterm, a=0, b=99999):
    'Generate WebSoc documents with valid coursecode ranges.'
    document = get_valid_document(yearterm, a, b)
    if document == None:
        m = (a + b) // 2
        if a < m < b:
            for document in iter_valid_documents(yearterm, a, m):
                yield document
            for document in iter_valid_documents(yearterm, m, b):
                yield document
    elif 'Whoa pardner' in document:
        raise StopIteration
    elif 'No courses matched' not in document:
        yield document

def get_valid_document(yearterm, a, b):
    'Get a WebSoc document given a valid coursecode range or return None.'
    coursecodes = '{}-{}'.format(a, b)
    document = post(yearterm, coursecodes)
    if 'please refine your search' not in document:
        return document

def post(yearterm, coursecodes):
    'Post a request to WebSoc and return the response.'
    url = 'https://www.reg.uci.edu/perl/WebSoc'
    query_template = '?YearTerm={}&CourseCodes={}&Submit=Text'
    query = query_template.format(yearterm, coursecodes)
    return urlfetch.fetch(url + query).content
