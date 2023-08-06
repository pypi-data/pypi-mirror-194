# 基础示例3
from tkforms import tkguna
from tkinter import Tk

root = Tk()
button = tkguna.Button()
button.configure(animated=True)  # animated设置是否有动画效果
button.configure(border_radius=5)  # border_radius设置圆角大小
button.pack(fill="both", expand="yes", padx=5, pady=5)
root.mainloop()