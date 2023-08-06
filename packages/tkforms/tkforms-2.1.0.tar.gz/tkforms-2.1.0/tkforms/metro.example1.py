from tkinter import Tk, Frame
from tkforms import tkmetro


root = Tk()
root.geometry("240x660")
root.configure(background="white")

frame1 = Frame(root, background="#ffffff")
frame1.pack(fill="both", expand="yes", padx=10, pady=10)

frame2 = Frame(root, background="#111111")
frame2.pack(fill="both", expand="yes", padx=10, pady=10)

btn1 = tkmetro.Button(frame1, text="button1")
btn1.pack(fill="both", expand="yes", padx=10, pady=10)

btn2 = tkmetro.Button(frame2, text="button2")
btn2.configure(theme='dark')
btn2.pack(fill="both", expand="yes", padx=10, pady=10)

cb1 = tkmetro.CheckBox(frame1, text="checkbox1")
cb1.pack(fill="both", expand="yes", padx=10, pady=10)

cb2 = tkmetro.CheckBox(frame2, text="checkbox2")
cb2.configure(theme="dark", checkstate="indeterminate")
cb2.pack(fill="both", expand="yes", padx=10, pady=10)

cbb1 = tkmetro.ComboBox(frame1)
cbb1.add_items({"Item1", "Item2"})
cbb1.clear()
cbb1.add_items({"Item3", "Item4"})
cbb1.insert(1, "Item5")
cbb1.remove("Item5")
cbb1.remove_at(1)
cbb1.pack(fill="both", expand="yes", padx=10, pady=10)

cbb2 = tkmetro.ComboBox(frame2)
cbb2.configure(theme="dark")
cbb2.add_items({"Item1", "Item2", "Item3", "Item4"})
cbb2.pack(fill="both", expand="yes", padx=10, pady=10)

text1 = tkmetro.Text(frame1)
text1.configure(multiline=True)
text1.pack(fill="both", expand="yes", padx=10, pady=10)

text2 = tkmetro.Text(frame2)
text2.configure(multiline=True, theme="dark")
text2.pack(fill="both", expand="yes", padx=10, pady=10)

datetime1 = tkmetro.DateTime(frame1)
datetime1.configure(value=[2023, 2, 25, 0, 0, 0, 0])
datetime1.pack(fill="both", expand="yes", padx=10, pady=10)

datetime2 = tkmetro.DateTime(frame2)
datetime2.configure(value=[2023, 2, 25, 0, 0, 0, 0], theme="dark")
datetime2.pack(fill="both", expand="yes", padx=10, pady=10)

trackbar1 = tkmetro.TrackBar(frame1)
trackbar1.pack(fill="both", expand="yes", padx=10, pady=10)

trackbar2 = tkmetro.TrackBar(frame2)
trackbar2.configure(theme="dark")
trackbar2.pack(fill="both", expand="yes", padx=10, pady=10)

root.mainloop()