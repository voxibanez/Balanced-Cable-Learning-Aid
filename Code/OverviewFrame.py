#!/usr/bin/python
from tkinter import *
import math
import WaveForms

top = None


class WinHandler(Tk):
        overviewFrameMain = NONE
        def __init__(self, *args, **kwargs):
                Tk.__init__(self, *args, **kwargs)
                container = Frame(self)
                self.geometry("500x600")
                self.title("Wave Degredation Tester")
                container.pack(side="top", fill="both", expand = True)

                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)

                self.frames = {}
                #Create permanent variable for main frame since it needs to be refreshed

                for F in (WaveFrame, SourceFrame):
                    page_name = F.__name__
                    frame = F(parent=container, controller=self)
                    self.frames[page_name] = frame
                    frame.grid(row=0, column=0, sticky="nsew")

                self.overviewFrameMain = OverviewFrame(parent=container, controller=self)
                self.frames["OverviewFrame"] = self.overviewFrameMain
                self.overviewFrameMain.grid(row=0, column=0, sticky="nsew")


                self.show_frame("OverviewFrame", container)

        def show_frame(self, cont, container=None):
            ####    Need to figure out why it will not switch back to overview  #########
            if cont is "OverviewFrame" and container != None:
                self.overviewFrameMain.refresh(container, self)
                frame = self.overviewFrameMain
                frame.tkraise()
            else:
                frame = self.frames[cont]
                frame.tkraise()




class OverviewFrame(Frame):
        var1 = None
        var2 = None
        var3 = None

        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.var1 = StringVar()
            self.var2 = StringVar()
            self.var3 = StringVar()
            var4 = StringVar()
            var4.set("test23")
            Label(self, text="OverviewFrame").pack(pady=10, padx=10)
            Label(self, textvariable=self.var1).pack(pady=10, padx=10)
            Label(self, textvariable=self.var2).pack(pady=10, padx=10)


            self.var1.set("Selected Waveform: ")
            self.var2.set("Selected Source: Source " + str(SourceFrame.sourceSelection))

            MenuFrame(self, controller, parent).pack(anchor="nw", side="left", fill="y", expand=True)

        def refresh(self, parent, controller):
            self.var1.set("Selected Waveform: ")
            self.var2.set("Selected Source: Source " + str(SourceFrame.sourceSelection))


class WaveFrame(Frame):
        funcSelection = 1
        def __init__(self, parent, controller):
                Frame.__init__(self, parent)
                Label(self, text="WaveFrame").pack(pady=10, padx=10)
                MenuFrame(self, controller, parent).pack(anchor="nw", side="left", fill="y", expand=True)
                self.buildWavesList(self.getWaves())

        def buildWavesList(self, waveGenFunctions):
            for funcCount in range(0, len(waveGenFunctions)):
                Radiobutton(self, text=(waveGenFunctions[funcCount]), variable=self.funcSelection, value=funcCount).pack(anchor="nw")

        def getWaves(self):
            #Waveforms can be created in the WaveForms class
            return WaveForms.getFunctions()




class SourceFrame(Frame):
        sourceSelection = 1
        def __init__(self, parent, controller):
                Frame.__init__(self, parent)
                Label(self, text="SourceFrame").pack(pady=10, padx=10)
                MenuFrame(self, controller, parent).pack(anchor="nw", side="left", fill="y", expand=True)
                self.buildSourceList(self.getSources())

        def buildSourceList(self, sources):
            for source in sources:
                Radiobutton(self, text=("Source " + str(source)), variable=self.sourceSelection, value=source).pack(
                    anchor="n")
        def getSources(self):
            # Sources will be populated by the number of outputs in the DAC
            sources = [1, 2, 3, 4, 5]
            return sources




class MenuFrame(Frame):
    def __init__(self, parent, controller, parent2):
        Frame.__init__(self, parent)
        Label(self, text="Menu").pack(pady=10, padx=10)
        Button(self, text='Source Selection', command=lambda: controller.show_frame("SourceFrame")).pack()
        Button(self, text='Wave Type', command=lambda: controller.show_frame("WaveFrame")).pack(anchor="nw", pady=20)
        Button(self, text='Overview', command=lambda: controller.show_frame("OverviewFrame", parent2)).pack(anchor="nw", pady=20)



def main():
        win = WinHandler()
        win.mainloop()