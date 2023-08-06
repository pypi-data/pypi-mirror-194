import clr
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")
from System.Drawing import Point, Size, Color, Font
from System.Windows.Forms import Panel

from tkinter import Frame


class Widget(Frame):
    def __init__(self, *args, width=100, height=30, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self._init_widget()
        from tkinter import _default_root
        self.bind("<Configure>", self._configure_widget)
        self.bind("<Map>", self._map)
        self.bind("<Unmap>", self._unmap)

        def click(*args, **kwargs):
            self.event_generate("<<Click>>")

        def double_click(*args, **kwargs):
            self.event_generate("<<DoubleClick>>")

        def enter(*args, **kwargs):
            self.event_generate("<<Enter>>")

        def leave(*args, **kwargs):
            self.event_generate("<<Leave>>")

        def up(*args, **kwargs):
            self.event_generate("<<Up>>")

        def down(*args, **kwargs):
            self.event_generate("<<Down>>")

        self._widget.Click += click
        self._widget.DoubleClick += double_click
        self._widget.MouseEnter += enter
        self._widget.MouseLeave += leave
        self._widget.MouseDown += down
        self._widget.MouseUp += up

        self.tk_forms(self, self._widget)
        self._widget.Visible = False

    def widget(self):
        return self._widget

    def tk_forms(self, parent, child):  # 将Winform组件添加入Tkinter组件
        from ctypes import windll
        windll.user32.SetParent(int(str(child.Handle)),
                                windll.user32.GetParent(parent.winfo_id()))  # 调用win32设置winform组件的父组件

    def state(self, state=None):
        if state == "active":
            self._widget.Enabled = True
        elif state == "disabled":
            self._widget.Enabled = False
        else:
            return self._widget.Enabled

    def configure(self, **kwargs):
        if "background" in kwargs:
            color = kwargs.pop("background")
            self._widget.FillColor = Color.FromArgb(color[0], color[1], color[2], color[3])
        if "foreground" in kwargs:
            color = kwargs.pop("foreground")
            self._widget.FillColor = Color.FromArgb(color[0], color[1], color[2], color[3])
        elif "border_color" in kwargs:
            color = kwargs.pop("border_color")
            self._widget.RectColor = Color.FromArgb(color[0], color[1], color[2], color[3])
        try:
            super().configure(**kwargs)
        except:
            pass

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "background":
            return self._widget.BackColor.A, self._widget.BackColor.R, self._widget.BackColor.G, self._widget.BackColor.B
        elif attribute_name == "border_color":
            return self._widget.RectColor.A, self._widget.RectColor.R, self._widget.RectColor.G, self._widget.RectColor.B
        elif attribute_name == "state":
            state = self._widget.Enabled
            if state:
                return "active"
            else:
                return "disabled"
        else:
            return super().cget(attribute_name)

    def font(self, name: str = "Sego UI", size: int = 9):
        try:
            font = Font(name, size)
        except TypeError:
            pass
        else:
            self._widget.Font = font

    def _map(self, _=None):
        self._widget.Visible = True

    def _unmap(self, _=None):
        self._widget.Visible = False

    def _configure_widget(self, _=None):
        self._widget.Location = Point(self.winfo_x(), self.winfo_y())
        self._widget.Size = Size(self.winfo_width(), self.winfo_height())

    def _init_widget(self):
        self._widget = None


from tkforms.metroframework import MetroUI as tkmetro
from tkforms.gunaui2 import GunaUI2 as tkguna
from tkforms.hzhcontrols import HZHControls as tkhzh


if __name__ == '__main__':
    from tkinter import Tk, Frame, Button

    root = Tk()
    frame = Control()
    frame.pack()
    root.mainloop()