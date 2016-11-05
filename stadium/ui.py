import urwid
import urwidgets
import utility

class ListDialogController(object):
    def __init__(self, dialog, cancel, select):
        self._widget = dialog
        self._cancel_func = cancel
        self._select_func = select

    def cancel(self):
        self._cancel_func()

    def enter(self, value):
        self._select_func(value)

class ListDialog(urwid.Overlay):
    def __init__(self, widgets, bottom_widget, cancel, select):
        self.controller = ListDialogController(
            self, cancel, select
        )

        self.cancel = urwidgets.MappedWrap(
            urwid.Text('Cancel'),
            'item', 'item_active',
        )
        self.cancel.keymap['enter'] = self.controller.cancel

        self._option_list = urwidgets.MappedPile(
            widgets
        )

        def selected_value():
            value = self._option_list.focus.text
            self.controller.enter(value)

        self._option_list.keymap['enter'] = selected_value


        self.pile = urwidgets.MappedPile(
            [self._option_list,
            urwid.Divider('-'),
            self.cancel]
        )

        lb = urwid.LineBox(self.pile)

        urwid.connect_signal(self._option_list, 'bottom', self.pile.shiftDown)

        super(ListDialog, self).__init__(lb, bottom_widget, 'center', 10, 'middle', 'pack')

    def shiftTop(self):
        self._option_list.top()
        self.pile.top()

    def shiftBottom(self):
        self._option_list.bottom()
        self.pile.bottom()

    def shiftUp(self):
        if self.cancel is self.pile.focus:
            self.pile.shiftUp()
        else:
            self._option_list.shiftUp()
        self.pile.shiftUp()

    def shiftDown(self):
        self._option_list.shiftDown()

class LeftRightLayout(urwid.TextLayout):
    def __init__(self, left, right):
        self.left = len(left)
        self.right = len(right)

    def layout(self, text, width, align, wrap):
        return [
            [(self.left, 0, self.left),
             (width - self.right - self.left, self.left),
             (self.right, self.left, self.left + self.right + 1)]
        ]

    def setRight(self, text):
        self.right = len(text)


class LeftRightWidget(urwid.WidgetWrap):
    def __init__(self, left_string, right_string):
        self.left_string = left_string
        self.right_string = right_string
        self.lay = LeftRightLayout(left_string, right_string)
        self.textWidget = urwid.Text(left_string + right_string, layout=self.lay)

        super(LeftRightWidget, self).__init__(self.textWidget)

    def setRight(self, string):
        self.lay.setRight(string)
        self.textWidget.set_text("%s%s" % (self.left_string, string))

    def setLeft(self, string):
        pass


class LabeledMeter(urwid.WidgetWrap):
    def __init__(self, label, left_bound, right_bound,
                 normal, complete,
                 initial=0, shiftAmount=1,
                 selectable=True, keymap={}):
        self.progress = urwid.ProgressBar(
            normal, complete,
            current=initial,
            done=right_bound
        )

        self.keymap = dict(keymap)
        self._s = selectable
        self.shiftAmount = shiftAmount

        self.scroll = utility.scroll(xrange(left_bound, right_bound + 1), initial - left_bound)

        self.label = LeftRightWidget(label, str(self.progress.current))

        self.pile = urwid.Pile([self.label, self.progress])

        super(LabeledMeter, self).__init__(self.pile)

    def selectable(self):
        return self._s

    def keypress(self, size, key):
        key = super(LabeledMeter, self).keypress(size, key)
        if key in self.keymap:
            key = self.keymap[key]()
        return key

    def decrement(self, amount=1):
        if self.progress.current != self.scroll(-amount * self.shiftAmount):
            self.progress.set_completion(self.scroll())
            self.label.setRight(str(self.progress.current))
            urwid.emit_signal(self, 'shift', self.progress.current)

    def increment(self, amount=1):
        if self.progress.current != self.scroll(amount * self.shiftAmount):
            self.progress.set_completion(self.scroll())
            self.label.setRight(str(self.progress.current))
            urwid.emit_signal(self, 'shift', self.progress.current)

    def _set_completion(self, completion):
        current = self.scroll(completion - self.scroll())
        self.progress.set_completion(current)
        self.label.setRight(str(current))
        
    def set_completion(self, completion):
        self._set_completion(completion)
        urwid.emit_signal(self, 'shift', completion)

urwid.register_signal(LabeledMeter, 'shift')
