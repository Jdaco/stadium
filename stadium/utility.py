import itertools

# String Completion
def complete(iterable, start_string):
    hits = [
        item[len(start_string):]
        for item in iterable
        if item[:len(start_string)] == start_string
    ]
    if len(hits) == 0:
        return start_string
    else:
        return start_string + ''.join([
            char[0] for char in
            itertools.takewhile(
                lambda x: len(set(x)) == 1,
                itertools.izip(*hits)
            )
        ])

# Add "lace" between each item in iterable
def inner_lace(iterable, lace):
    r = [
        i
        for item in
        itertools.izip(
            iterable, itertools.repeat(lace)
        )
        for i in item
    ]
    if r:
        r.pop(-1)
    return r

# Reverse Enumerate
def renumerate(iterable):
    return (
        (index, iterable[index])
        for index in
        xrange(len(iterable) - 1, -1, -1)
    )

# Simple function chaining
def chain(*args):
    def inner():
        for arg in args:
            arg()
    return inner

# Decorator that returns last value if no args
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
    
# Scrollbar Functionality - Inputs change the position in a collection
@cached_coroutine
def scroll(collection, initial=0):
    if len(collection) == 0:
        raise ValueError("Collection cannot be empty")
    if initial < 0 or initial > len(collection):
        raise IndexError("Initial index is out of bounds")
    max_length = len(collection) - 1
    index = initial
    while True:
        recieved = (yield collection[index])
        index += recieved
        if index < 0:
            index = 0
        elif index > max_length:
            index = max_length
