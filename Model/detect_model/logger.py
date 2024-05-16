import logging
from io import StringIO

log_capture_string = StringIO()
logger = logging.getLogger('ultralytics')
stream_handler = logging.StreamHandler(log_capture_string)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

def get_log_time():
    log_contents = log_capture_string.getvalue()
    log_capture_string.seek(0)
    log_capture_string.truncate()
    log_contents = log_contents.split(",")[2]
    log_contents = log_contents.split("m")[0]
    log_contents = float(log_contents)
    return log_contents