import clr
from tkforms.metroframework import metro_lib, metro_fonts_lib, metro_design_lib
clr.AddReference(metro_lib)
clr.AddReference(metro_fonts_lib)
clr.AddReference(metro_design_lib)
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from MetroFramework.Controls import (MetroButton, MetroCheckBox, MetroComboBox,
                                     MetroDateTime, MetroLabel, MetroTextBox,
                                     MetroTrackBar, MetroProgressBar, MetroToggle,
                                     MetroTile)
from MetroFramework import MetroThemeStyle, MetroColorStyle
from MetroFramework.Components import MetroToolTip
from System.Drawing import Point, Size, ContentAlignment
from System.Windows.Forms import CheckState
from tkforms import Widget


__all__ = [
    "LIGHT",
    "DARK",
    "MetroBase",
    "Button",
    "ComboBox",
    "DateTime"
    "Label",
    "Panel",
    "Text",
    "ToolTip",
    "TrackBar"
]

LIGHT = "light"
DARK = "dark"

INDETERMINATE = "indeterminate"
CHECKED = "checked"
UNCHECKED = "unchecked"


class MetroBase(Widget):
    def configure(self, **kwargs):
        if "theme" in kwargs:
            style = kwargs.pop("theme")
            if style == "light":
                self._widget.Theme = MetroThemeStyle.Light
            elif style == "dark":
                self._widget.Theme = MetroThemeStyle.Dark
        elif "style" in kwargs:
            style = kwargs.pop("style")
            if style == "default":
                self._widget.Style = MetroColorStyle.Default
            elif style == "black":
                self._widget.Style = MetroColorStyle.Black
            elif style == "white":
                self._widget.Style = MetroColorStyle.White
            elif style == "silver":
                self._widget.Style = MetroColorStyle.Silver
            elif style == "blue":
                self._widget.Style = MetroColorStyle.Blue
            elif style == "green":
                self._widget.Style = MetroColorStyle.Green
            elif style == "lime":
                self._widget.Style = MetroColorStyle.Lime
            elif style == "teal":
                self._widget.Style = MetroColorStyle.Teal
            elif style == "orange":
                self._widget.Style = MetroColorStyle.Orange
            elif style == "brown":
                self._widget.Style = MetroColorStyle.Brown
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "theme":
            style = self._widget.Theme
            if style == MetroThemeStyle.Light:
                return "light"
            elif style == MetroThemeStyle.Dark:
                return "dark"
        else:
            return super().cget(attribute_name)


class Button(MetroBase):
    def __init__(self, *args, width=100, height=30, text="MetroControl.Button", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroButton()

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)


class ComboBox(MetroBase):
    def __init__(self, *args, width=100, height=30, text="MetroControl.ComboBox", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroComboBox()

    def configure(self, **kwargs):
        if "item_height" in kwargs:
            self._widget.ItemHeight = kwargs.pop("item_height")
        elif "text" in kwargs:
            self._widget.PromptText = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "item_height":
            return self._widget.ItemHeight
        elif attribute_name == "text":
            return self._widget.PromptText
        else:
            return super().cget(attribute_name)

    def add(self, item: str):
        self._widget.Items.Add(item)

    def add_items(self, items: tuple):
        self._widget.Items.AddRange(items)

    def clear(self):
        self._widget.Items.Clear()

    def insert(self, index: int, item: str):
        self._widget.Items.Insert(index, item)

    def remove(self, item: str):
        self._widget.Items.Remove(item)

    def remove_at(self, index: int):
        self._widget.Items.RemoveAt(index)

    def count(self):
        return self._widget.Items.Count

    def index(self, item: str):
        return self._widget.Items.IndexOf(item)


class CheckBox(MetroBase):
    def __init__(self, *args, width=100, height=30, text="MetroControl.CheckBox", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroCheckBox()

        def checked_changed(*args, **kwargs):
            self.event_generate("<<CheckedChanged>>")

        def check_state_changed(*args, **kwargs):
            self.event_generate("<<CheckStateChanged>>")

        self._widget.CheckedChanged += checked_changed
        self._widget.CheckStateChanged += check_state_changed

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        elif "checked" in kwargs:
            self._widget.Checked = kwargs.pop("checked")
        elif "checkstate" in kwargs:
            check_state = kwargs.pop("checkstate")
            if check_state == "indeterminate":
                self._widget.CheckState = CheckState.Indeterminate
            elif check_state == "checked":
                self._widget.CheckState = CheckState.Checked
            elif check_state == "unchecked":
                self._widget.CheckState = CheckState.Unchecked
        elif "checkalign" in kwargs:
            check_align = kwargs.pop("checkalign")
            if check_align == "left":
                self._widget.CheckAlign = ContentAlignment.MiddleLeft
            elif check_align == "right":
                self._widget.CheckAlign = ContentAlignment.MiddleRight
            elif check_align == "top":
                self._widget.CheckState = ContentAlignment.TopCenter
            elif check_align == "bottom":
                self._widget.CheckState = ContentAlignment.BottomCenter
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text
        elif attribute_name == "checked":
            return self._widget.Checked
        elif attribute_name == "checkstate":
            check_state = self._widget.CheckState
            if check_state == CheckState.Indeterminate:
                return "indeterminate"
            elif check_state == CheckState.Checked:
                return "checked"
            elif check_state == CheckState.Unchecked:
                return "unchecked"
            return
        else:
            return super().cget(attribute_name)


class DateTime(MetroBase):
    def __init__(self, *args, width=100, height=30, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        def value_changed(*args, **kwargs):
            self.event_generate("<<ValueChanged>>")

        self._widget.ValueChanged += value_changed

    def _init_widget(self):
        self._widget = MetroDateTime()

    def configure(self, **kwargs):
        if "value" in kwargs:
            value = kwargs.pop("value")
            from System import DateTime
            self._widget.Value = DateTime(value[0], value[1], value[2])
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "value":
            date = self._widget.Value
            return (date.Year, date.Month, date.Day)
        else:
            return super().cget(attribute_name)

class Label(MetroBase):
    def __init__(self, *args, width=100, height=30, text="MetroControl.Label", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroLabel()

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)


class ProgressBar(MetroBase):
    def __init__(self, *args, width=100, height=30, text="MetroControl.CheckBox", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroProgressBar()

    def step(self):
        self._widget.PerformStep()

    def configure(self, **kwargs):
        if "value" in kwargs:
            self._widget.Value = kwargs.pop("value")
        elif "maximum" in kwargs:
            self._widget.Maximum = kwargs.pop("maximum")
        elif "minimum" in kwargs:
            self._widget.Minimum = kwargs.pop("minimum")
        elif "step" in kwargs:
            self._widget.Step = kwargs.pop("step")
        elif "animation" in kwargs:
            self._widget.MarqueeAnimationSpeed = kwargs.pop("animation")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "value":
            return self._widget.Value
        elif attribute_name == "maximum":
            return self._widget.Maximum
        elif attribute_name == "minimum":
            return self._widget.Minimum
        elif attribute_name == "step":
            return self._widget.Step
        elif attribute_name == "animation":
            return self._widget.MarqueeAnimationSpeed
        else:
            return super().cget(attribute_name)


class RadioButton(CheckBox):
    def __init__(self, *args, width=100, height=30, text="MetroControl.RadioButton", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroCheckBox()

        def checked_changed(*args, **kwargs):
            self.event_generate("<<CheckedChanged>>")

        def check_state_changed(*args, **kwargs):
            self.event_generate("<<CheckStateChanged>>")

        self._widget.CheckedChanged += checked_changed
        self._widget.CheckStateChanged += check_state_changed


class Tile(MetroBase):
    def __init__(self, *args, width=100, height=30, text="MetroControl.Tile", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroTile()


class Text(MetroBase):
    def __init__(self, *args, width=100, height=30, text="MetroControl.Text", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroTextBox()

    def configure(self, **kwargs):
        if "multiline" in kwargs:
            self._widget.Multiline = kwargs.pop("multiline")
        elif "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "multiline":
            return self._widget.Multiline
        elif attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)


class TrackBar(MetroBase):
    def __init__(self, *args, width=100, height=30, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _init_widget(self):
        self._widget = MetroTrackBar()

        def changed(*args, **kwargs):
            self.event_generate("<<ValueChanged>>")

        self._widget.ValueChanged += changed

    def configure(self, **kwargs):
        if "value" in kwargs:
            self._widget.Value = kwargs.pop("value")
        elif "maximum" in kwargs:
            self._widget.Maximum = kwargs.pop("maximum")
        elif "minimum" in kwargs:
            self._widget.Minimum = kwargs.pop("minimum")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "value":
            return self._widget.Value
        elif attribute_name == "maximum":
            return self._widget.Maximum
        elif attribute_name == "minimum":
            return self._widget.Minimum
        else:
            return super().cget(attribute_name)


class ToolTip(object):
    def __init__(self):
        self._init_widget()

    def _init_widget(self):
        self._widget = MetroToolTip()

    def widget(self):
        return self._widget

    def configure(self, **kwargs):
        if "theme" in kwargs:
            style = kwargs.pop("theme")
            if style == "light":
                self._widget.Theme = MetroThemeStyle.Light
            elif style == "dark":
                self._widget.Theme = MetroThemeStyle.Dark
        elif "style" in kwargs:
            style = kwargs.pop("style")
            if style == "default":
                self._widget.Style = MetroColorStyle.Default
            elif style == "black":
                self._widget.Style = MetroColorStyle.Black
            elif style == "white":
                self._widget.Style = MetroColorStyle.White
            elif style == "silver":
                self._widget.Style = MetroColorStyle.Silver
            elif style == "blue":
                self._widget.Style = MetroColorStyle.Blue
            elif style == "green":
                self._widget.Style = MetroColorStyle.Green
            elif style == "lime":
                self._widget.Style = MetroColorStyle.Lime
            elif style == "teal":
                self._widget.Style = MetroColorStyle.Teal
            elif style == "orange":
                self._widget.Style = MetroColorStyle.Orange
            elif style == "brown":
                self._widget.Style = MetroColorStyle.Brown

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "theme":
            style = self._widget.Theme
            if style == MetroThemeStyle.Light:
                return "light"
            elif style == MetroThemeStyle.Dark:
                return "dark"

    def set_tooltip(self, widget: Widget, message: str):
        self._widget.SetToolTip(widget.widget(), message)


class Toggle(CheckBox):
    def __init__(self, *args, width=100, height=30, text="MetroControl.Toggle", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = MetroToggle()

        def checked_changed(*args, **kwargs):
            self.event_generate("<<CheckedChanged>>")

        def check_state_changed(*args, **kwargs):
            self.event_generate("<<CheckStateChanged>>")

        self._widget.CheckedChanged += checked_changed
        self._widget.CheckStateChanged += check_state_changed


if __name__ == '__main__':
    from tkinter import Tk, Frame

    root = Tk()
    root.configure(background="white")

    frame1 = Frame(root, background="#ffffff")
    frame1.pack(fill="both", expand="yes")

    frame2 = Frame(root, background="#111111")
    frame2.pack(fill="both", expand="yes")

    tile1 = Tile(frame1, text="tile1")
    tile1.pack(fill="both", expand="yes", padx=4, pady=4)

    tile2 = Tile(frame2, text="tile2")
    tile2.configure(theme='dark')
    tile2.pack(fill="both", expand="yes", padx=4, pady=4)

    btn1 = Button(frame1, text="button1")
    btn1.pack(fill="both", expand="yes", padx=4, pady=4)

    btn2 = Button(frame2, text="button2")
    btn2.configure(theme='dark')
    btn2.pack(fill="both", expand="yes", padx=4, pady=4)

    cb1 = CheckBox(frame1, text="checkbox1")
    cb1.pack(fill="both", expand="yes", padx=4, pady=4)

    cb2 = CheckBox(frame2, text="checkbox2")
    cb2.configure(theme="dark", checkstate="indeterminate")
    cb2.pack(fill="both", expand="yes", padx=4, pady=4)

    cbb1 = ComboBox(frame1)
    cbb1.add_items({"Item1", "Item2"})
    cbb1.clear()
    cbb1.add_items({"Item3", "Item4"})
    cbb1.insert(1, "Item5")
    cbb1.remove("Item5")
    cbb1.remove_at(1)
    cbb1.pack(fill="both", expand="yes", padx=4, pady=4)

    cbb2 = ComboBox(frame2)
    cbb2.configure(theme="dark")
    cbb2.add_items({"Item1", "Item2", "Item3", "Item4"})
    cbb2.pack(fill="both", expand="yes", padx=4, pady=4)

    text1 = Text(frame1)
    text1.configure(multiline=True)
    text1.pack(fill="both", expand="yes", padx=4, pady=4)

    text2 = Text(frame2)
    text2.configure(multiline=True, theme="dark")
    text2.pack(fill="both", expand="yes", padx=4, pady=4)

    datetime1 = DateTime(frame1)
    datetime1.configure(value=[2023, 2, 25, 0, 0, 0, 0])
    datetime1.pack(fill="both", expand="yes", padx=4, pady=4)

    datetime2 = DateTime(frame2)
    datetime2.configure(value=[2023, 2, 25, 0, 0, 0, 0], theme="dark")
    datetime2.pack(fill="both", expand="yes", padx=4, pady=4)

    toggle1 = RadioButton(frame1)
    toggle1.pack(fill="both", expand="yes", padx=4, pady=4)

    toggle2 = RadioButton(frame2)
    toggle2.configure(theme="dark", checkstate="indeterminate")
    toggle2.pack(fill="both", expand="yes", padx=4, pady=4)

    toggle1 = Toggle(frame1)
    toggle1.pack(fill="both", expand="yes", padx=4, pady=4)

    toggle2 = Toggle(frame2)
    toggle2.configure(theme="dark", checkstate="indeterminate")
    toggle2.pack(fill="both", expand="yes", padx=4, pady=4)

    trackbar1 = TrackBar(frame1)
    trackbar1.pack(fill="both", expand="yes", padx=4, pady=4)

    trackbar2 = TrackBar(frame2)
    trackbar2.configure(theme="dark")
    trackbar2.pack(fill="both", expand="yes", padx=4, pady=4)

    root.mainloop()