from tkinter import *
def main():
    root = Tk()
    Message(root, text=("Select a waveform")).grid(row=0, column=0, columnspan=5)
    Message(root, text=("Select another waveform")).grid(row=0, columnspan=5, column=10)

    root.mainloop()
    root.destroy()