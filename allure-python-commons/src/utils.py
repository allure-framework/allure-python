import time
import uuid
import hashlib


def md5(case_name):
    case_name = case_name.encode('utf-8')
    m = hashlib.md5()
    m.update(case_name)
    return m.hexdigest()


def uuid4():
    return str(uuid.uuid4())


def now():
    return int(round(1000 * time.time()))
