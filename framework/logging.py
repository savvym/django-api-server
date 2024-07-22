import logging
from framework.static import _tls

class request_idFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(_tls, 'request_id', 'MAIN')
        return True