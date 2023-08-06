import clr
from tkforms.gunaui2 import gunaui2_lib
clr.AddReference(gunaui2_lib)
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
import pythonnet
from Guna.UI2.WinForms import Guna2Button, Guna2ComboBox, \
    Guna2Chip, Guna2CircleButton, \
    Guna2ControlBox, Guna2GradientButton, \
    Guna2TrackBar, Guna2CheckBox, \
    Guna2CustomCheckBox, Guna2TextBox, \
    Guna2MessageDialog, MessageDialogStyle, \
    MessageDialogIcon, GunaUI_LicenseMgr, \
    Guna2DateTimePicker, Guna2DragControl, \
    Guna2NumericUpDown
from Guna.UI2.WinForms.Enums import TextBoxStyle, ButtonMode
from System.Drawing import Color
from System.Windows.Forms import Form
from tkforms import Widget

DEFAULT = "default"
MATERIAL = "material"

TOGGLE = "toggle"
RADIO = "radio"

LIGHT = "light"
DARK = "dark"

ERROR = "error"
QUESTION = "question"
WARNING = "warning"
INFORMATION = "information"

__all__ = [
    "DEFAULT",
    "TOGGLE"
    "MATERIAL",
    "LIGHT",
    "DARK",
    "ERROR",
    "QUESTION",
    "WARNING",
    "INFORMATION",
    "Button",
    "CheckBox",
    "Chip",
    "CircleButton",
    "ComboBox",
    "ControlBox",
    "CustomCheckBox",
    "DateTimePicker",
    "GradientButton",
    "GunaBase",
    "LicenseDialog",
    "MessageDialog",
    "SpinBox",
    "TextBox",
    "TrackBar",
]


class GunaBase(Widget):
    def configure(self, **kwargs):
        if "auto_rounded" in kwargs:
            self._widget.AutoRoundedCorners = kwargs.pop("auto_rounded")
        elif "animated" in kwargs:
            self._widget.Animated = kwargs.pop("animated")
        elif "border" in kwargs:
            self._widget.BorderThickness = kwargs.pop("border")
        elif "border_color" in kwargs:
            color = kwargs.pop("border_color")
            self._widget.BorderColor = Color.FromArgb(color[0], color[1], color[2], color[3])
        elif "border_radius" in kwargs:
            self._widget.BorderRadius = kwargs.pop("border_radius")
        elif "background2" in kwargs:
            self._widget.FillColor2 = kwargs.pop("background2")
        elif "style" in kwargs:
            style = kwargs.pop("style")
            if style == "material":
                self._widget.Style = TextBoxStyle.Material
            elif style == "default":
                self._widget.Style = TextBoxStyle.Default

        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "auto_rounded":
            return self._widget.AutoRoundedCorners
        elif attribute_name == "animated":
            return self._widget.Animated
        elif attribute_name == "border":
            return self._widget.BorderThickness
        elif attribute_name == "border_radius":
            return self._widget.BorderRadius
        elif attribute_name == "background2":
            return self._widget.FillColor.A, self._widget.FillColor.R, self._widget.FillColor.G, self._widget.FillColor.B
        elif attribute_name == "style":
            style = self._widget.Style
            if style == TextBoxStyle.Material:
                return "material"
            elif style == TextBoxStyle.Default:
                return "default"
        else:
            return super().cget(attribute_name)

class Button(GunaBase):
    def __init__(self, *args, width=100, height=30, text="GunaUI2.Button", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.text = text

    def _init_widget(self):
        self._widget = Guna2Button()

        def checked(*args, **kwargs):
            self.event_generate("<<CheckedChanged>>")

        self._widget.CheckedChanged += checked

    def configure(self, **kwargs):
        if "mode" in kwargs:
            mode = kwargs.pop("mode")
            if mode == "default":
                self._widget.ButtonMode = ButtonMode.DefaultButton
            elif mode == "toggle":
                self._widget.ButtonMode = ButtonMode.ToogleButton
            elif mode == "radio":
                self._widget.ButtonMode = ButtonMode.RadioButton
        if "checked" in kwargs:
            self._widget.Checked = kwargs.pop("checked")
        elif "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "checked":
            return self._widget.Checked
        elif attribute_name == "mode":
            mode = self._widget.ButtonMode
            if mode == ButtonMode.DefaultButton:
                return "default"
            elif mode == ButtonMode.ToogleButton:
                return "toggle"
            elif mode == ButtonMode.RadioButton:
                return "radio"
        elif attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)


class CheckBox(Button):
    def _init_widget(self):
        self._widget = Guna2CheckBox()

        def changed(*args, **kwargs):
            self.event_generate("<<CheckedChanged>>")

        self._widget.CheckedChanged += changed

    def configure(self, **kwargs):
        if "checked" in kwargs:
            self._widget.Checked = kwargs.pop("checked")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "checked":
            return self._widget.Checked
        else:
            return super().cget(attribute_name)

class CustomCheckBox(CheckBox):
    def _init_widget(self):
        self._widget = Guna2CustomCheckBox()


class Chip(Button):
    def _init_widget(self):
        self._widget = Guna2Chip()


class CircleButton(Button):
    def _init_widget(self):
        self._widget = Guna2CircleButton()


class ComboBox(GunaBase):
    def __init__(self, *args, width=100, height=30, text="MetroControl.ComboBox", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.text = text

    def _init_widget(self):
        self._widget = Guna2ComboBox()

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


class ControlBox(Button):
    def _init_widget(self):
        self._widget = Guna2ControlBox()


class DragControl:
    def __init__(self, target: Widget = None):
        self._init_widget()
        self.configure(target=target)

    def _init_widget(self):
        self._widget = Guna2DragControl()

    def configure(self, target: Widget = None):
        if target is not None:
            self._widget.TargetControl = target.widget()

    config = configure


class Form:
    def __init__(self):
        self._init_widget()

    def _init_widget(self):
        self._widget = Form()

    def widget(self):
        return self._widget


class GradientButton(Button):
    def _init_widget(self):
        self._widget = Guna2GradientButton()


class LicenseDialog:
    def __init__(self):
        self._init_widget()

    def _init_widget(self):
        self._widget = GunaUI_LicenseMgr()

    def widget(self):
        return self._widget


class MessageDialog:
    def __init__(self, icon=None, text="GunaUI2.MessageDialog", theme=DEFAULT):
        self._init_widget()
        self.configure(icon=icon, text=text, theme=theme)

    def _init_widget(self):
        self._widget = Guna2MessageDialog()

    def font(self, name: str = "Sego UI", size: int = 9):
        try:
            font = Font(name, size)
        except TypeError:
            pass
        else:
            self._widget.Font = font

    def configure(self, font=None, icon=None, text=None, theme=None):
        if font is not None:
            try:
                from System.Drawing import Font
                font = Font(font[0], font[1])
            except TypeError:
                pass
            else:
                self._widget.Font = font
                self._widget.Font = font
        elif icon is not None:
            if icon == "error":
                self._widget.Icon = MessageDialogIcon.Error
            elif icon == "question":
                self._widget.Icon = MessageDialogIcon.Question
            elif icon == "warning":
                self._widget.Icon = MessageDialogIcon.Warning
            elif icon == "information":
                self._widget.Icon = MessageDialogIcon.Information
        elif theme is not None:
            if theme == "default":
                self._widget.Style = MessageDialogStyle.Default
            elif theme == "light":
                self._widget.Style = MessageDialogStyle.Light
            elif theme == "dark":
                self._widget.Style = MessageDialogStyle.Dark
        elif text is not None:
            self._widget.Text = text

    config = configure

    def cget(self, attribute_name):
        if attribute_name == "theme":
            theme = self._widget.Style
            if theme == MessageDialogStyle.Default:
                return "default"
            elif theme == MessageDialogStyle.Light:
                return "light"
            elif theme == MessageDialogStyle.Dark:
                return "dark"
        elif attribute_name == "text":
            return self._widget.Text

    def widget(self):
        return self._widget

    def show(self):
        self._widget.Show()


class SpinBox(GunaBase):
    def _init_widget(self):
        self._widget = Guna2NumericUpDown()


class TextBox(Button):
    def _init_widget(self):
        self._widget = Guna2TextBox()

        def changed(*args, **kwargs):
            self.event_generate("<<TextChange>>")

        self._widget.TextChanged += changed

    def configure(self, **kwargs):
        if "multiline" in kwargs:
            self._widget.Multiline = kwargs.pop("multiline")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "multiline":
            return self._widget.Multiline
        else:
            return super().cget(attribute_name)


class DateTimePicker(Button):
    def _init_widget(self):
        self._widget = Guna2DateTimePicker()


class TrackBar(GunaBase):
    def _init_widget(self):
        self._widget = Guna2TrackBar()

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


if __name__ == '__main__':
    from tkinter import Tk, font, Frame
    from tkforms.toolbar import ToolBar
    root = Tk()
    from tkinter import Wm
    root.configure(background="#1d262c")
    root.geometry("250x360")

    btn1 = Button()
    btn1.configure(text="Hello", background=(255, 32, 164, 255), foreground=(255, 32, 164, 255))
    btn1.pack(fill="x")

    btn2 = Button()
    btn2.configure(background=(255, 137, 13, 255))
    btn2.pack(fill="x")

    root.mainloop()