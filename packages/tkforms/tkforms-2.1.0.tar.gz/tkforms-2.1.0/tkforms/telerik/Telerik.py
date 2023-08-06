import clr
from tkforms.telerik import list
for index in list:
    if index.split(".")[-1] == "dll":
        clr.AddReference(index)
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from Telerik.WinControls.UI import RadButton
from System.Drawing import Point, Size
from tkforms import Widget


class BaseTelerik(Widget):
    pass


class Button(BaseTelerik):
    def __init__(self, *args, width=100, height=30, text="MetroControl.Button", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadButton()


if __name__ == '__main__':
    from tkinter import Tk
    root = Tk()
    btn1 = Button()
    btn1.pack()
    root.mainloop()