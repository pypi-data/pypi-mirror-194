# 基础示例2
from tkforms import tkmetro
from tkinter import Tk

root = Tk()
button1 = tkmetro.Button()
button1.pack(fill="both", expand="yes", padx=5, pady=5)
button2 = tkmetro.Button()
button2.configure(theme="dark")  # theme设置组件主题配色，可设置为 "light" 或 "dark"
button2.pack(fill="both", expand="yes", padx=5, pady=5)
root.mainloop()