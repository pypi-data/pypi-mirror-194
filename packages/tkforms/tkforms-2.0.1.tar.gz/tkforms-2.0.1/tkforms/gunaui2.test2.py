# 基础示例2
from tkforms import tkguna
from tkinter import Tk

root = Tk()
button = tkguna.Button()
button.configure(animated=True, auto_rounded=True)  # animated设置是否有动画效果 auto_rounded自动设置圆角的大小
button.pack(fill="both", expand="yes", padx=5, pady=5)
root.mainloop()