#!/usr/bin/python2
from stadium import ui
import pytest
import mock

class TestListDialogController:
    def test_cancel_calls_callback(self):
        # Cancel should call cancel_func
        a = []

        def cancel_func():
            a.append('cancelled')
        
        def select_func():
            a.append('selected')

        sut = ui.ListDialogController(None, cancel_func, select_func)

        sut.cancel()

        assert len(a) == 1
        assert a[0] == 'cancelled'

    def test_enter_calls_callback(self):
        # enter() should call select function with value
        a = []

        def cancel_func():
            a.append('cancelled')
        
        def select_func(value):
            a.append(value)

        sut = ui.ListDialogController(None, cancel_func, select_func)

        sut.enter("Option 1")
        
        assert len(a) == 1
        assert a[0] == "Option 1"

class TestLabeledMeterController:
    def setup_method(self):
        self.left_bound = 0
        self.right_bound = 100
        self.initial = 50
        self.shift_amount = 10

        self.widget = mock.Mock()
        self.widget._set_completion = mock.Mock()

        self.sut = ui.LabeledMeterController(
            self.widget,
            self.left_bound, self.right_bound,
            self.initial, self.shift_amount,
        )

    def test_decrement_full(self):
        self.sut.decrement(2)

        self.widget._set_completion.assert_called_once_with(self.initial - self.shift_amount * 2)

    def test_decrement_stopped(self):
        # Decrement shouldn't go past left_bound
        self.sut.decrement(20)

        self.widget._set_completion.assert_called_once_with(self.left_bound)

    def test_increment_full(self):
        self.sut.increment(2)

        self.widget._set_completion.assert_called_once_with(self.initial + self.shift_amount * 2)

    def test_increment_stopped(self):
        # Increment shouldnt' go past right_bound
        self.sut.increment(20)

        self.widget._set_completion.assert_called_once_with(self.right_bound)

    def test_set_completion(self):
        self.sut.set_completion(10)

        self.widget._set_completion.assert_called_once_with(10)

    def test_set_completion_below_lower(self):
        # Set_completion shouldn't go below left_bound
        self.sut.set_completion(
            self.left_bound - 100
        )

        self.widget._set_completion.assert_called_once_with( self.left_bound )

    def test_set_completion_above_upper(self):
        # Set_completion shouldn't go above right_bound
        self.sut.set_completion(
            self.right_bound + 100
        )

        self.widget._set_completion.assert_called_once_with( self.right_bound )


