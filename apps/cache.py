__author__ = 'windy'


cache = dict()


def get(key):
    return cache.get(key, None)


def put(key, value):
    cache[key] = value


def get_by_time(t1, t2):
    values = []
    find = False
    for k in cache:
        if t1 == k:
            find = True
        if find:
            values.append(get(k))
        if t2 == k:
            values.append(get(k))
            return values
    return values


