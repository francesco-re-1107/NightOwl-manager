import logging
import requests
import os

LOGGER = None

def get_logger():
    global LOGGER

    if LOGGER:
        return LOGGER
    
    logger = logging.getLogger("NightOwl-manager")
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(ch)

    LOGGER = logger

    return logger

def to_int(value, default=None):
    try:
        return int(value)
    except:
        return default
    
def to_float(value, default=None):
    try:
        return float(value)
    except:
        return default

def download_model(url, file_name):
    if os.path.isfile(file_name):
        return

    LOGGER.info(f"Downloading {url} to {file_name}")
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)