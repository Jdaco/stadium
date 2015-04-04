#!/usr/bin/python2
import sys
import itertools
import functools
import traceback
import urwid
import pyparsing as pp
import utility
import re


argument_regex = r"(?:'[^']*'|\"[^\"]*\"|[^\s'\"]+)"
command_regex = r'(?P<command>[^\s\'"]+)(?P<arguments>(?:\s+%s)*)' % argument_regex

def parse_command(command):
        match = re.match(self.command_regex, command)
        if match is None:
            return None
        arguments = [
            arg.strip('"\' ')
            for arg in
            re.findall(self.argument_regex, match.group('arguments'))
        ]
        return (
            match.group('command'),
            arguments,
        )

class MappedWrap(urwid.AttrMap):
    def __init__(self, widget,
                 attrmap=None, focusmap=None,
                 keymap={}, selectable=True,
                 *args, **kwargs):
        self._widget = widget
        self.keymap = dict(keymap)
        self._s = selectable

        super(MappedWrap, self).__init__(widget, attrmap, focusmap, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._widget, name)

    def __setattribute__(self, name, value):
        return setattr(self._widget, name, value)

    def keypress(self, size, key):
        if hasattr(self._widget, 'keypress'):
            key = self._widget.keypress(size, key)
        if key in self.keymap:
            key = self.keymap[key]()
        return key

    def selectable(self):
        return self._s

    @property
    def attrmap(self):
        return self.attr_map

    @attrmap.setter
    def attrmap(self, value):
        self.set_attr_map(value)

    @property
    def focusmap(self):
        return self.focus_map

    @focusmap.setter
    def focusmap(self, value):
        self.set_focus_map(value)


class CommandFrame(urwid.Frame):
    def __init__(self, body, header=None, focus_part='body'):
        command_line = urwid.Edit(multiline=False)
        self.command_line = MappedWrap(command_line)

        if not hasattr(self, 'keymap'):
            self.keymap = {}
        if not hasattr(self, 'commands'):
            self.commands = {}

        self.keymap[':'] = functools.partial(self.start_editing, callback=self.submit_command)

        super(CommandFrame, self).__init__(body, header, self.command_line, focus_part)

    def keypress(self, size, key):
        key = urwid.Frame.keypress(self, size, key)
        if key in self.keymap:
            self.keymap[key]()
        return key

    def submit_command(self, data):
        parse_result = parse_command(data)
        if parse_result is None:
            self.change_status("Invalid command")
        func, args = parse_result
        if func not in self.commands:
            self.change_status("Command not found")
        else:
            try:   
                self.commands[func](*args)
            except TypeError:
                # Too many arguments
                tb = traceback.extract_tb(sys.exc_info()[2])
                if len(tb) == 1:
                    self.changeStatus("Wrong number of arguments")
                else:
                    raise

    def stop_editing(self):
        self.command_line.set_caption('')
        self.command_line.set_edit_text('')
        self.focus_position = 'body'

    def start_editing(self, caption='> ', startText='', callback=None):
        self.command_line.set_caption(caption)
        self.command_line.set_edit_text(startText)
        self.footer = self.command_line
        self.focus_position = "footer"
        callback = self.submitCommand if callback is None else callback

        def enter_command():
            t = self.command_line.edit_text
            self.stop_editing()
            callback(t)

        self.command_line.keymap['esc'] = self.stop_editing
        self.command_line.keymap['enter'] = enter_command
        
    def change_status(self, stat):
        self.footer = urwid.Text(stat)


class MappedList(urwid.ListBox):
    def __init__(self, widgets=[], keymap={}, shiftFunc=None):
        self.scroll = utility.scroll(range(len(widgets)))
        self.widgets = widgets
        self.keymap = dict(keymap)
        self.shiftFunc = shiftFunc
        super(MappedList, self).__init__(urwid.SimpleFocusListWalker(widgets))

    def keypress(self, size, key):
        key = super(MappedList, self).keypress(size, key)
        if key in self.keymap:
            key = self.keymap[key](size)
        return key

    def top(self):
        self.set_focus(0)

    def bottom(self):
        self.set_focus(len(self.body) - 1)

    def shiftDown(self, size, amount=1):
        if self.body.focus is not self.scroll(amount):
            self.change_focus(size, self.scroll())
            self.set_focus_valign('middle')
            if self.shiftFunc:
                self.shiftFunc()

    def shiftUp(self, size, amount=1):
        if self.body.focus is not self.scroll(-amount):
            self.change_focus(size, self.scroll())
            self.set_focus_valign('middle')
            if self.shiftFunc:
                self.shiftFunc()

    def set(self, contents):
        self.body[:] = contents
        currentIndex = self.scroll()
        focusIndex = len(contents) - 1 \
            if len(contents) < currentIndex \
            else currentIndex
        self.scroll = utility.scroll(range(len(contents)), focusIndex)

    def set_focus(self, position):
        self.focus_position = position
        self.set_focus_valign('middle')
        self.body[:] = self.body[:]
        self.scroll = utility.scroll(range(len(self.body[:])), position)
        if self.shiftFunc:
            self.shiftFunc()

    def find(self, predicate, start=0, direction='forward'):
        total = len(self.body)
        indexes = xrange(start - total + 1, start + 1, 1) if direction == 'forward' \
            else xrange(start - 1, start - total, -1)
        for index in indexes:
            if predicate(self.body[index]):
                return index if index >= 0 else total + index
        return -1


class MappedPile(urwid.Pile):
    filler = urwid.Text("")

    def __init__(self, widgets=[],
                 keymap={}, hitTop=None, hitBottom=None,
                 shiftFunc=None, focus_item=None,
                 space=0, constraint=(lambda x, y: True)):
        self.keymap = dict(keymap)
        widgets = [item
                   for sublist in
                   zip(widgets,
                       *itertools.tee(
                           itertools.repeat(MappedPile.filler),
                           space
                           )
                       )
                   for item in sublist]
        self.constraint = constraint
        self.hitTop = hitTop
        self.hitBottom = hitBottom
        self.shiftFunc = shiftFunc
        super(MappedPile, self).__init__(widgets, focus_item)

    def keypress(self, size, key):
        # key = super(MappedPile, self).keypress(size, key)
        if self.focus.selectable():
            item_rows = self.get_item_rows(size, focus=True) \
                if len(size) == 2 else None
            tsize = self.get_item_size(size, self.focus_position,
                                       True, item_rows)
            key = self.focus.keypress(tsize, key)
        if key in self.keymap:
            key = self.keymap[key]()
        return key

    def top(self):
        for index in xrange(0, len(self.contents)):
            widget = self.contents[index][0]
            if widget is not MappedPile.filler and self.constraint(index, widget):
                self.focus_position = index
                return
    
    def bottom(self):
        for index in xrange(len(self.contents) - 1, -1, -1):
            widget = self.contents[index][0]
            if widget is not MappedPile.filler and self.constraint(index, widget):
                self.focus_position = index
                return

    def shiftDown(self, amount=1):
        try:
            nextIndex = (
                index for index, widget in
                enumerate([cont[0] for cont in self.contents])
                if index > self.focus_position
                and widget is not MappedPile.filler
                and self.constraint(index, widget)
                ).next()
            self.focus_position = nextIndex
        except StopIteration:
            if self.hitBottom is not None:
                self.hitBottom()

    def shiftUp(self, amount=1):
        try:
            nextIndex = (
                index for index, widget in
                reversed(
                    tuple(
                        enumerate([cont[0] for cont in self.contents])
                    )
                )
                if index < self.focus_position
                and widget is not MappedPile.filler
                and self.constraint(index, widget)
                ).next()
            self.focus_position = nextIndex
        except StopIteration:
            if self.hitTop is not None:
                self.hitTop()

    def selectable(self):
        return reduce(
            (lambda x, y: x | y),
            [widget.selectable() for widget, options in self.contents]
        )

    def isEmpty(self):
        return len(self.contents) == 0

    def add(self, widget):
        self.contents.append((widget, self.options()))
        if len(self.contents) == 1:
            self.focus_position = 0

    def set(self, widgets):
        self.contents = [(widget, self.options()) for widget in widgets]


class TitledPile(MappedPile):
    def __init__(self, title=urwid.Text(''), widgets=[], *args, **kwargs):
        self.title = title
        widgets = [title] + widgets
        super(TitledPile, self).__init__(widgets, *args, **kwargs)
        if not self.isEmpty():
            self.focus_position = 1

    def shiftUp(self):
        if self.focus_position > 1:
            super(TitledPile, self).shiftUp()
        elif self.hitTop is not None:
            self.hitTop()

    def isEmpty(self):
        return len(self.contents) == 1

    def add(self, widget):
        self.contents.append((widget, self.options()))
        if len(self.contents) == 2:
            self.focus_position = 1
            print 'yes'

    def set(self, widgets):
        super(TitledPile, self).set((self.title,) + tuple(widgets))
        if len(self.contents) >= 2:
            self.focus_position = 1

    def setTitle(self, widget):
        self.title = widget
        self.contents[0] = (widget, self.options())
