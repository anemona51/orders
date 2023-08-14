import random
from threading import Timer


def delayed(f):
    seconds = round(random.uniform(0.1, 1.0), 10)

    def wrapper(*args, **kargs):
        t = Timer(seconds, f, args, kargs)
        t.start()

    return wrapper
