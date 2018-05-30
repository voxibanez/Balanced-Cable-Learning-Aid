from tkinter import *
import math


top = Tk()
def quitClick1():
        self.top.destroy()
        MainWindow.open()

def open():
        main()

def main():
        top = Tk()
        top.title("Wave Degredation Tester")
        top.geometry("500x1000")

        width = 500
        height = 200
        center = height // 2
        x_increment = 1
        # width stretch
        x_factor = 0.02
        # height stretch
        y_amplitude = 80

        c = Canvas(width=400, height=300, bg='white')
        c.pack()

        c.create_text(10, 20, anchor=SW)

        center_line = c.create_line(0, center, width, center, fill='green')

        # create the coordinate list for the sin() curve, have to be integers
        xy1 = []
        for x in range(400):
            # x coordinates
            xy1.append(x * x_increment)
            # y coordinates
            xy1.append(int(math.sin(x * x_factor) * y_amplitude) + center)

        sin_line = c.create_line(xy1, fill='blue')

        Message(text="Set frequency").pack()
        Text(width=100, height = 20).pack()
        Button(top, text='Quit', command=quitClick1).pack(fill=X)

        top.mainloop()