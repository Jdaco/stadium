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
