import clr
from tkforms.metroframework import metro_lib, metro_fonts_lib, metro_design_lib
clr.AddReference(metro_lib)
clr.AddReference(metro_fonts_lib)
clr.AddReference(metro_design_lib)
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from MetroFramework.Controls import MetroButton, MetroComboBox, MetroLabel, MetroPanel, MetroTextBox, MetroDateTime, MetroTrackBar
from MetroFramework import MetroThemeStyle, MetroColorStyle
from MetroFramework.Components import MetroToolTip
from System.Drawing import Point, Size
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


class DateTime(MetroBase):
    def __init__(self, *args, width=100, height=30, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _init_widget(self):
        self._widget = MetroDateTime()

    def configure(self, **kwargs):
        if "value" in kwargs:
            value = kwargs.pop("value")
            from System import DateTime
            self._widget.Value = DateTime(value[0], value[1], value[2], value[3], value[4], value[5], value[6])
        super().configure(**kwargs)


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


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.configure(background="white")

    tooltip1 = ToolTip()

    btn1 = Button(root, text="button1")
    btn1.pack(fill="both", expand="yes", padx=10, pady=10)

    btn2 = Button(root, text="button2")
    btn2.configure(theme='dark')
    btn2.pack(fill="both", expand="yes", padx=10, pady=10)

    tooltip1.set_tooltip(btn2, "Metro Button1")

    cbb1 = ComboBox(root)
    cbb1.configure(style="green")
    cbb1.add_items({"Item1", "Item2"})
    cbb1.clear()
    cbb1.add_items({"Item3", "Item4"})
    cbb1.insert(1, "Item5")
    cbb1.remove("Item5")
    cbb1.remove_at(1)
    cbb1.pack(fill="both", expand="yes", padx=10, pady=10)

    cbb2 = ComboBox(root)
    cbb2.configure(theme="dark", style="green")
    cbb2.add_items({"Item1", "Item2", "Item3", "Item4"})
    cbb2.pack(fill="both", expand="yes", padx=10, pady=10)

    text1 = Text(root)
    text1.configure(multiline=True)
    text1.pack(fill="both", expand="yes", padx=10, pady=10)

    datetime1 = DateTime(root)
    datetime1.configure(value=[2023, 2, 25, 0, 0, 0, 0])
    datetime1.pack(fill="both", expand="yes", padx=10, pady=10)

    trackbar1 = TrackBar(root)
    trackbar1.pack(fill="both", expand="yes", padx=10, pady=10)

    root.mainloop()