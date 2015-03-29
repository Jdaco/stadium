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
    
def coroutine(func):
    def inner(*args, **kwargs):
        wrapped = func(*args, **kwargs)
        wrapped.next()

        def new_interface(*args):
            return wrapped.send(*args)
        return new_interface
    return inner

@coroutine
def StateMachine(state):
    recieved = None
    key = None
    while True:
        key = (yield key if recieved is None else None)
        recieved = state(key)
        state = recieved if recieved is not None else state

def ChainedTransition(func, transition):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        return transition()
    return inner

def Transition(func, state):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        return state
    return inner

class State(object):
    def __init__(self, default_func=None, wraps=None):
        self.func = default_func if default_func is not None \
            else lambda x: None
        self.wraps = wraps
        self.edges = {}
    
    def __call__(self, char):
        if char in self.edges:
            return self.edges[char]()
        elif self.wraps:
            return self.wraps(char)
        self.func(char)
    
    def add_edge(self, char, tran):
        self.edges[char] = tran


def capWord(string):
    words = (word.capitalize() for word in string.split())
    return ' '.join(words)

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


@cached_coroutine
def repeat(collection, initial=0):
    length = len(collection)
    index = initial
    while True:
        recieved = (yield collection[index]) % length
        index = ((length + recieved) + index) % length
