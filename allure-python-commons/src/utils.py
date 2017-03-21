import time
import uuid


def uuid4():
    return str(uuid.uuid4())


def now():
    return int(round(1000 * time.time()))
