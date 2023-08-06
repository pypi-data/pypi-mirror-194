import csv as _csv


class Dialect(csv.Dialect):
    delimiter = '\t'
    doublequote = False
    escapechar = None
    lineterminator = '\n'
    quotechar = '"'
    quoting = _csv.QUOTE_NONE
    skipinitialspace = False
    strict = True

def reader(data):
    return _csv.reader(data, dialect=Dialect)

def writer(data):
    return _csv.writer(data, dialect=Dialect)


