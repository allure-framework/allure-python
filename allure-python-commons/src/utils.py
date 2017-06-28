import time
import uuid
import hashlib


def md5(*args):
    m = hashlib.md5()
    for arg in args:
        part = arg.encode('utf-8')
        m.update(part)
    return m.hexdigest()


def uuid4():
    return str(uuid.uuid4())


def now():
    return int(round(1000 * time.time()))
