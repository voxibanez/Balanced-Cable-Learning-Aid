import OverviewFrame
import SigMonitor
import bak
import Test
import VirtualXLRSimulator
import RealXLRSimulator
import theBackupPlan
from tkinter import *
import soundfile as sf

class Window(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["Main"] = bak.Application(container, self)
        self.frames["Main"].grid(row=0, column=0, sticky="nsew")
        self.frames["RealXLR"] = RealXLRSimulator.start(sf.read("sin_1000Hz.wav"), container, self)
        self.frames["RealXLR"].grid(row=0, column=0, sticky="nsew")
        self.frames["VirtualXLR"] = VirtualXLRSimulator.start(sf.read("sin_1000Hz.wav"), container, self)
        self.frames["VirtualXLR"].grid(row=0, column=0, sticky="nsew")
        self.frames["CompFiles"] = theBackupPlan.letsGo(container, self)
        self.frames["CompFiles"].grid(row=0, column=0, sticky="nsew")


            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.


        self.show_frame("Main")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


#Test.main()
#bak.main()

main = Window()
main.mainloop()