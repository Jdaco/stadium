import urwid
import urwidgets
import utility

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


class LeftRightWidget(urwidgets.MappedText):
    def __init__(self, left_string, right_string, *args, **kwargs):
        self.left_string = left_string
        self.right_string = right_string
        self.lay = LeftRightLayout(left_string, right_string)

        super(LeftRightWidget, self).__init__(left_string + right_string, layout=self.lay, *args, **kwargs)

    def setRight(self, string):
        self.lay.setRight(string)
        self.textWidget.set_text("%s%s" % (self.left_string, string))

    def setLeft(self, string):
        pass


class LabeledMeter(urwid.WidgetWrap):
    def __init__(self, label, left_bound, right_bound,
                 normal, complete,
                 initial=0, shiftAmount=1,
                 shiftFunc=None, selectable=True,
                 keymap={}):
        self.progress = urwid.ProgressBar(normal, complete,
                                          current=initial,
                                          done=right_bound)

        self.keymap = dict(keymap)
        self._s = selectable
        self.shiftAmount = shiftAmount

        self.scroll = utility.scroll(xrange(left_bound, right_bound + 1), initial - left_bound)

        self.shiftFunc = shiftFunc

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
        self.progress.set_completion(self.scroll(-amount * self.shiftAmount))
        self.label.setRight(str(self.progress.current))
        if self.shiftFunc:
            self.shiftFunc(self.progress.current)

    def increment(self, amount=1):
        self.progress.set_completion(self.scroll(amount * self.shiftAmount))
        self.label.setRight(str(self.progress.current))
        if self.shiftFunc:
            self.shiftFunc(self.progress.current)

    def set_completion(self, completion):
        current = self.scroll(completion - self.scroll())
        self.progress.set_completion(current)
        self.label.setRight(str(current))


class SelectableWrapper(urwid.WidgetWrap):
    def __init__(self, widget, selectable=True):
        self._selectable = selectable
        super(SelectableWrapper, self).__init__(widget)

    def selectable(self):
        return True
