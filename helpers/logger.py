from datetime import datetime

log_callback = None
DEBUG = False


def _emit(msg):
    if log_callback:
        log_callback(msg)
    print(msg)

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    _emit(f"{ts} {msg}")


def debug(msg):
    if DEBUG:
        ts = datetime.now().strftime("%H:%M:%S")
        _emit(f"{ts} [DEBUG] {msg}")