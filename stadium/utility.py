import itertools

def inner_lace(iterable, lace):
    r = [
        i
        for item in
        itertools.izip(
            iterable, itertools.repeat(lace)
        )
        for i in item
    ]
    r.pop(-1)
    return r
def renumerate(iterable):
    return (
        (index, iterable[index])
        for index in
        xrange(len(iterable) - 1, -1, -1)
    )

def chain(*args):
    def inner():
        for arg in args:
            arg()
    return inner

def cached_coroutine(func):
    cache = {}
    def inner(*args, **kwargs):
        wrapped = func(*args, **kwargs)
        cache[wrapped] = wrapped.next()

        def interface(*args):
            if len(args) != 0:
                cache[wrapped] = wrapped.send(*args)
            return cache[wrapped]
        return interface
    return inner
    
@cached_coroutine
def scroll(collection, initial=0):
    max_length = len(collection) - 1
    index = initial
    while True:
        recieved = (yield collection[index])
        index += recieved
        if index < 0:
            index = 0
        elif index > max_length:
            index = max_length
