import tkinter as tk


window = tk.Tk()
window.title("Testing window")
button = tk.Button(window, text="Press me!", width=25, command=window.destroy)
button.pack()
window.mainloop()