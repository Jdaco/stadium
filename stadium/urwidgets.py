#!/usr/bin/python2
import urwid
import sys
import traceback
import pyparsing as pp
import itertools
import utility
import functools
import itertools


class MappedWrap(urwid.AttrMap):
    def __init__(self, widget,
                 attrmap=None, focusmap=None,
                 keymap={}, selectable=True,
                 *args, **kwargs):
        self.widget = widget
        self.keymap = dict(keymap)
        self._s = selectable

        super(MappedWrap, self).__init__(widget, attrmap, focusmap, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.widget, name)

    def __setattribute__(self, name, value):
        return setattr(self.widget, name, value)

    def keypress(self, size, key):
        key = self.widget.keypress(size, key)
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


class MappedText(MappedWrap):
    def __init__(self, text, layout=None,
                 *args, **kwargs):
        self.textWidget = urwid.Text(text, layout=layout)
        super(MappedText, self).__init__(self.textWidget, *args, **kwargs)

    def keypress(self, size, key):
        if key in self.keymap:
            key = self.keymap[key]()
        return key

    @property
    def text(self):
        return self.textWidget.text

    def set_text(self, text):
        self.textWidget.set_text(text)


class CommandFrame(urwid.Frame):
    argument = pp.Or((pp.Word(pp.printables), pp.QuotedString("'")))
    command = pp.Word(pp.printables)
    commandLine = command + pp.ZeroOrMore(argument)
    functions = {}
    keymap = {}

    def __init__(self, body=None, header=None, focus_part='body'):
        edit = urwid.Edit(multiline=False)
        self.edit = MappedWrap(edit)
        self.functions = dict(self.functions)
        keymap = dict(self.keymap)

        self.keymap[':'] = functools.partial(self.startEditing, callback=self.submitCommand)

        urwid.Frame.__init__(self, body, header, self.edit, focus_part)

    def keypress(self, size, key):
        key = urwid.Frame.keypress(self, size, key)
        if key in self.keymap:
            self.keymap[key]()
        return key

    def submitCommand(self, data):
        arguments = CommandFrame.commandLine.parseString(data).asList()
        function = arguments.pop(0)
        try:
            self.functions[function](*arguments)
        except TypeError:
            # Too many arguments
            tb = traceback.extract_tb(sys.exc_info()[2])
            if len(tb) == 1:
                self.changeStatus("Wrong number of arguments")
            else:
                raise
        except KeyError:
            # Command not found
            tb = traceback.extract_tb(sys.exc_info()[2])
            if len(tb) == 1:
                self.changeStatus("Command not found")
            else:
                raise

    def stopEditing(self):
        self.edit.set_caption('')
        self.edit.set_edit_text('')
        self.focus_position = 'body'

    def startEditing(self, caption='> ', startText='', callback=None):
        self.edit.set_caption(caption)
        self.edit.set_edit_text(startText)
        self.footer = self.edit
        self.focus_position = "footer"
        callback = self.submitCommand if callback is None else callback

        def enter_command():
            t = self.edit.edit_text
            self.stopEditing()
            callback(t)

        self.edit.keymap['esc'] = self.stopEditing
        self.edit.keymap['enter'] = enter_command
        
    def changeStatus(self, stat):
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
