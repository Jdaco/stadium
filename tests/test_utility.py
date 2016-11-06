#!/usr/bin/python2
from stadium import utility
import pytest

class TestInnerLace:
    def test_empty(self):
        # Empty iterable should return empty list
        iterable = ()
        lace = 1
        
        laced_iterable = utility.inner_lace(iterable, lace)

        assert len(laced_iterable) == 0

    def test_single(self):
        # Iterable with one item should return single item list
        iterable = ([],)
        lace = 1

        laced_iterable = utility.inner_lace(iterable, lace)

        assert len(laced_iterable) == 1
        assert laced_iterable[0] is iterable[0]

    def test_count(self):
        # Length should be len(iterable) * 2 - 1

        iterable = xrange(10) 
        lace = 'lace'

        laced_iterable = utility.inner_lace(iterable, lace)

        assert len(laced_iterable) == 19
    def test_lacing(self):
        # Every other item should be lace

        iterable = range(10) 
        lace = 'lace'

        laced_iterable = utility.inner_lace(iterable, lace)

        for index, item in enumerate(laced_iterable):
            if index % 2 == 0 and item is not iterable[index / 2]:
                pytest.fail("Item: ( %s ) at Index: ( %s ) does not match original item" % (repr(item), repr(index)))
            elif index % 2 == 1 and item is not lace:
                pytest.fail("Item: ( %s ) at Index: ( %s ) does not match lace item" % (repr(item), repr(index)))
        
class TestChain:
    def test_order(self):
        # Each funciton gets called in order

        a = [0]
        b = [0]
        c = [0]
        def change_a():
            a[0] = b[0] + c[0] + 1
        
        def change_b():
            b[0] = a[0] + c[0] + 1

        def change_c():
            c[0] = a[0] + b[0] + 1


        chain = utility.chain(change_a, change_b, change_c)
        chain()

        assert a[0] == 1
        assert b[0] == 2
        assert c[0] == 4

    def test_no_args(self):
        # Passing no arguments should not throw exception
        chain = utility.chain()
        chain()

class TestRenumerate:
    def test_empty(self):
        # Empty iterator should return empty iterator
        re = utility.renumerate( () )

        assert len(list(re)) == 0

    def test_single(self):
        # Iterator with single item should return same as enumerate

        values = (10,)

        re = tuple(utility.renumerate(values))

        assert len(re) == 1
        assert re[0][0] is 0 
        assert re[0][1] is values[0]

    def test_order(self):
        # Index should match original object
        
        values = ([], [], [])

        re = utility.renumerate(values)

        for index, item in re:
            assert values[index] is item

    def test_reverse(self):
        # Index should be descending starting from len(iterable) - 1
        values = ([], [], [])

        re = utility.renumerate(values)

        for index, re_item in enumerate(re):
            assert index + re_item[0] == len(values) - 1

    def test_length(self):
        # Length should be same as original iterable
        values = ([], [], [])

        re = utility.renumerate(values)

        assert len(list(re)) == len(values)

class TestComplete:
    def test_empty_iterable_empty_string(self):
        # empty iterable, empty string should return empty string
        iterable = tuple()
        start_string = ''

        sut = utility.complete(iterable, start_string)

        assert sut == ''

    def test_empty_iterable(self):
        # empty iterable should return start_string
        iterable = tuple()
        start_string = 'alpha'

        sut = utility.complete(iterable, start_string)

        assert sut == start_string

    def test_empty_string(self):
        # empty string should return empty string
        iterable = ('alpha', 'beta', 'delta')
        start_string = ''

        sut = utility.complete(iterable, start_string)

        assert sut == start_string

    def test_no_matches(self):
        #no matches should return start string
        iterable = ('alpha', 'beta', 'omega')
        start_string = 'delta'
        
        sut = utility.complete(iterable, start_string)

        assert sut == start_string

    def test_single_match(self):
        # if there is a single match return that match
        iterable = ('alpha' ,'alphaomega', 'alph')
        start_string =  'alphao'

        sut = utility.complete(iterable, start_string)

        assert sut == 'alphaomega'
        

    def test_single_match_contained_word(self):
        # If the iterable contains words containing other words, complete to the most unique string
        iterable = ('alphaomega', 'beta', 'alpha')
        start_string = 'alp'

        sut = utility.complete(iterable, start_string)

        assert sut == 'alpha'

    def test_multiple_match(self):
        # If there are multiple matches, return the most unique string
        iterable = ('alpha', 'alphaomega', 'alphist')
        start_string = 'a'

        sut = utility.complete(iterable, start_string)
        
        assert sut == 'alph'

class TestCachedCoroutine:
    def test_starts_coroutine(self):
        # Creating the generator should call next() on coroutine
        a = []
        def coroutine():
            a.append('yes')
            recieved = (yield 'no')

        # Simulates decorator
        sut = utility.cached_coroutine(coroutine)
        # Creates generator
        sut()

        assert a[0] == 'yes'

    def test_no_args_cached(self):
        # Sending no args to coroutine should return last returned value
        def coroutine():
            recieved = None
            while True:
                recieved = (yield recieved)

        func = utility.cached_coroutine(coroutine)
        sut = func()
        sut(10)
        sut(20)
        sut(30)
        value = sut()

        assert value == 30

    def test_same_value_keeps_calling(self):
        # Sending the same value multiple times should still run routine, no return cached
        a = []
        def coroutine():
            recieved = None
            while True:
                recieved = (yield recieved)
                a.append(recieved)

        func = utility.cached_coroutine(coroutine)
        sut = func()
        sut(10)
        sut(10)
        sut(10)
        sut(10)
        sut(10)

        assert len(a) == 5
        assert len(set(a)) == 1
        assert set(a).pop() == 10


class TestScroll:
    def test_empty_exception(self):
        # Function throws ValueError on empty collection
        collection = []

        with pytest.raises(ValueError):
            sut = utility.scroll(collection, 0)

    def test_single_item_never_changes(self):
        # With a single-item-collection it should always be on that item
        collection = (0,)
        sut = utility.scroll(collection, 0)

        sut(-10)
        sut(5)
        value = sut()

        assert value == collection[0]

    def test_starts_at_initial(self):
        # The 2nd parameter determines the staring position
        collection = range(10)
        initial = 5
        sut = utility.scroll(collection, initial)

        value = sut()

        assert value == collection[initial]

    def test_initial_above_max(self):
        # Initial > len(collection) should raise IndexError
        collection = range(10)
        
        with pytest.raises(IndexError):
            sut = utility.scroll(collection, 20)

    def test_initial_below_zero(self):
        # Intial < 0 should raise IndexError
        collection = range(10)

        with pytest.raises(IndexError):
            sut = utility.scroll(collection, -20)

    def test_check_position(self):
        # After sending movement, position should change
        collection = range(10)
        sut = utility.scroll(collection, 0)

        sut(5)
        value = sut()

        assert value == collection[5]

    def test_scroll_past_bottom(self):
        # Input past the first item should stay at the first item
        collection = range(10)
        initial = 0
        sut = utility.scroll(collection, initial)

        value = sut(-20)

        assert value == 0

    def test_scroll_past_top(self):
        # Inputting past the last item should stay at the last item
        collection = range(10)
        initial = 0
        sut = utility.scroll(collection, initial)

        value = sut(20)

        assert value == 9


class TestCapitalizeMove:
    def test_one_word(self):
        string = 'thunderwave'
        
        sut = utility.capitalize_move(string)

        assert sut == 'Thunderwave'

    def test_hypen(self):
        string = 'thunder-wave'
        
        sut = utility.capitalize_move(string)

        assert sut == 'Thunder-Wave'

    def test_multiple_words(self):
        string = 'thunder wave'
        
        sut = utility.capitalize_move(string)

        assert sut == 'Thunder Wave'

    def test_empty_string(self):
        string = ''
        
        sut = utility.capitalize_move(string)

        assert sut == ''

    def test_all_caps(self):
        string = 'THUNDERWAVE'
        
        sut = utility.capitalize_move(string)

        assert sut == 'Thunderwave'




