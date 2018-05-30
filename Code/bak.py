#!/usr/bin/python
from tkinter import *
import math
import theBackupPlan
import WaveForms
import wave
import random
import struct
import Algos
import RealXLRSimulator
import SigMonitor
import VirtualXLRSimulator
import Driver_Interop

import soundfile as sf
top = Tk()

class Application(Frame):
        audioBoardPresent = False
        sourceSelection = IntVar()
        funcSelection = IntVar()
        version = "0.1 Proof of Concept"
        def createWidgets(self):
                waveGenFunctions = WaveForms.getFunctions()
                #Set display message
                Message(self, text=("Wave degredation tester V" + self.version), width = 400).pack()

                #Make start the quit buttons
                if self.audioBoardPresent:
                        Button(self, text='Start', command=self.xlrReal).pack(fill=X)
                else:
                        Button(self, text='Start (Audio Board Not Detected)',state=DISABLED , command=self.xlrReal).pack(fill=X)
                Button(self, text='Compare files', command=self.backup).pack(fill=X)
                Button(self, text='Virtual XLR Simulator', command=self.xlrSim).pack(fill=X)
                Button(self, text='Quit',command=self.quitClick).pack(fill=X)

        def quitClick(self):
                print("Not implemented")
        def backup(self):
                self.controller.show_frame("CompFiles")

        def xlrSim(self):
                #self.controller.show_frame("VirtualXLR")
                self.controller.show_frame("RealXLR")

        def xlrReal(self):
                self.controller.show_frame("RealXLR")

        def __init__(self, master, controller):
                Frame.__init__(self, master)
                self.controller = controller
                self.grid()
                self.audioBoardPresent = Driver_Interop.checkSoundboard()
                self.createWidgets()



def createSine():
        c = Canvas(width=400, height=300, bg='white')
        c.pack()
        width = 500
        height = 200
        center = height//2
        x_increment = 1
        # width stretch
        x_factor = 0.02
        # height stretch
        y_amplitude = 80

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