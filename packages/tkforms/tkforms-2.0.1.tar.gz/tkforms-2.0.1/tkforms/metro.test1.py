# 基础示例1
from tkforms import tkmetro
from tkinter import Tk

root = Tk()
button = tkmetro.Button()
button.pack(fill="both", expand="yes", padx=5, pady=5)
root.mainloop()