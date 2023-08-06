from datetime import datetime
from dateutil.parser import parse as __dateparse

parse = __dateparse
"""parse php_date format

ex 1970-01-01T00:00:00Z"""

class __now:
    def __init__(self):
        pass

    @property
    def local(self):
        return datetime.now()

    @property
    def utc(self):
        return datetime.utcnow()

now = __now()