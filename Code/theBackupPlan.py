#!/usr/bin/python
import soundfile as sf
import sounddevice as sd
import wave
from tkinter import filedialog
from tkinter import *
import os
import struct
import Algos
import math
import tempfile


def quitClick():
    print("Not impl")

class letsGo(Frame):
    file_path1 = None
    file_path2 = None
    waveFile1 = None
    waveFile2 = None

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.grid()
        self.main()

    def startClick(self):
        diffAlgo(self.waveFile1, self.waveFile2).calculateDifference()

    def genClick(self):
        diffAlgo(self.waveFile1, self.waveFile2).audioDifference()
        #diffAlgo(self.waveFile1, self.waveFile2).audioSum()



    def canStart(self):
        if(self.file_path1 is not None and self.file_path2 is not None):
            self.startButton.config(state=NORMAL)
            self.genDiffButton.config(state=NORMAL)

    def openFile1(self):
        self.file_path1 = filedialog.askopenfilename()
        waveFile = wave.open(self.file_path1, 'r')
        #Use wave to get filename but store information in sf
        file1_info = "Filename: " + str(os.path.basename(self.file_path1)) + "; SampleRate: " + str(waveFile.getframerate()) + "; SampleWidth: " + str(waveFile.getsampwidth())
        self.label1.configure(text=file1_info)
        waveFile.close()

        samples, samplerate = sf.read(self.file_path1)
        self.waveFile1 = [samples, samplerate]
        self.canStart()

    def openFile2(self):
        self.file_path2 = filedialog.askopenfilename()
        waveFile = wave.open(self.file_path2, 'r')
        file2_info = "Filename: " + str(os.path.basename(self.file_path2)) + "; SampleRate: " + str(
            waveFile.getframerate()) + "; SampleWidth: " + str(waveFile.getsampwidth())
        self.label2.configure(text=file2_info)
        waveFile.close()

        samples, samplerate = sf.read(self.file_path2)
        self.waveFile2 = [samples, samplerate]
        self.canStart()

    def quitClick(self):
        self.controller.show_frame("Main")

    def main(self):

        file1_info = "No File Selected"
        file2_info = "No File Selected"
        #print(file1_info.get())

        Button(self, text='Browse1', command=self.openFile1).pack(anchor=W)
        self.label1 = Label(self, text="No file selected")
        self.label2 = Label(self, text="No file selected")
        self.label1.pack(fill=X)
        Button(self, text='Browse2', command=self.openFile2).pack(anchor=W)
        self.label2.pack(fill=X)
        self.startButton = Button(self, state=DISABLED, text='Get Degredation %')
        self.genDiffButton = Button(self, state=DISABLED, text='Generate Difference Audio')
        self.startButton.pack(fill=X)
        self.genDiffButton.pack(fill=X)
        Button(self, text='Quit', command=self.quitClick).pack(fill=X)
        self.startButton.configure(command=self.startClick)
        self.genDiffButton.configure(command=self.genClick)

class diffAlgo():
    wave1 = None
    wave2 = None

    def calculateDifference(self):
        array1 = self.wave1[0]
        array2 = self.wave2[0]

        diff = 0
        for index in range(0,len(array1)):
            diff += abs((array1[index]) - (array2[index]))
        diff /= len(array1)

        print("Differece: " + str(diff))

    def audioDifference(self):
        sd.play(Algos.calculateDifference(self.wave1[0], self.wave2[0]), self.wave1[1])



    def __init__(self, _wave1, _wave2):
        self.wave1 = _wave1
        self.wave2 = _wave2
