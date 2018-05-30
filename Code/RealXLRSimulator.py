import Algos
import random
from tkinter import *
import soundfile as sf
import sounddevice as sd
from copy import deepcopy
import random
import math
import time
import wave
import os
from tkinter import filedialog
import WaveForms
import Driver_Interop

class balanced:
    orig = []
    channel1 = []
    channel2 = []
    sampleRate = None
    def __init__(self, audio):
        self.orig = audio[0]
        self.sampleRate = audio[1]

    def changeAudio(self, switch):
        self.channel1 = []
        self.channel2 = []
        if switch.get() == 1:
            self.channel1 = [(x) for x in self.orig]
            self.channel2 = [(0) for x in self.orig]
        elif switch.get() == 2:
            self.channel1 = [(0) for x in self.orig]
            self.channel2 = [(x) for x in self.orig]
        elif switch.get() == 3:
            self.channel1 = [(x / 2) for x in self.orig]
            self.channel2 = [((x * -1) / 2) for x in self.orig]
        else:
            print("Error, switch out of range: " + str(switch))

    def differentiate(self):
        return Algos.calculateDifference(self.channel1, self.channel2)
        #return self.channel1

class noise:
    level = None
    randomness = None
    def __init__(self, level, randomness):
        self.level = level
        self.randomness = randomness

    def introduceNoiseBal(self, channel1, channel2):
        newChannel1 = [0] * len(channel1)
        newChannel2 = [0] * len(channel2)
        noise = [0] * len(channel1)
        for i in range(0, len(channel1)):
            if self.level == 0:
                value = 0
            else:
                value = random.uniform(-.0001 * (self.level * self.level), .0001 * (self.level * self.level))
            newChannel1[i] = Algos.clamp((channel1[i] + value), -1, 1)
            newChannel2[i] = Algos.clamp((channel2[i] + value), -1, 1)
            noise[i] = value

        return newChannel1, newChannel2, noise

    def introduceNoiseUnbal(self, channel):
        newChannel = [0] * len(channel)
        noise = [0] * len(channel)
        for i in range(0, len(channel)):
            if self.level == 0:
                value = 0
            else:
                value = random.uniform(-.0001 * (self.level * self.level), .0001 * (self.level * self.level))
            newChannel[i] =Algos.clamp((channel[i] + value), -1, 1)
            noise[i] = value

        return newChannel, noise

class unbalanced:
    channel = []
    sampleRate = None
    def __init__(self, audio):
        self.channel = audio[0]
        self.sampleRate = audio[1]

class start(Frame):
    balancedCable = None
    unbalancedCable = None
    balancedCableNoise = None
    unbalancedCableNoise = None
    bal = False
    unbal = False
    audioSamples = None

    c = None
    radioButtons = []
    radioButtonsIn = []
    radioButtonsOut = []
    ready = False


    noiseOn = False



    def __init__(self,audio, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.balChoice = IntVar(master=self)
        self.funcSelection = IntVar(master=self)
        self.sourceSelection = IntVar(master=self)
        self.unbalIn = IntVar(master=self)
        self.unbalOut = IntVar(master=self)
        self.balancedCable = balanced(audio)
        self.balancedCableNoise = balanced(audio)
        self.unbalancedCable = unbalanced(audio)
        self.audioSamples = audio[0]
        self.grid()
        self.main()


    def canGo(self):
        if (self.unbal) and (self.unbalOut.get() == 1 or self.unbalOut.get() == 2) and (self.unbalIn.get() == 1 or self.unbalIn.get() == 2):
            self.startButton.configure(state=NORMAL)
            self.stopButton.configure(state=NORMAL)
        elif (self.bal) and (self.balChoice.get() == 1 or self.balChoice.get() == 2 or self.balChoice.get() == 3):
            self.startButton.configure(state=NORMAL)
            self.stopButton.configure(state=NORMAL)
        else:
            self.startButton.configure(state=DISABLED)
            self.stopButton.configure(state=DISABLED)


    def setBalanced(self):
        self.createCanvasBal()
        for val in self.radioButtons:
            val.configure(state=NORMAL)
        for val in self.radioButtonsIn:
            val.configure(state=DISABLED)
        for val in self.radioButtonsOut:
            val.configure(state=DISABLED)
        self.bal = True
        self.unbal = False
        self.canGo()

    def setUnbalanced(self):
        self.createCanvasUnbal()
        for val in self.radioButtons:
            val.configure(state=DISABLED)
        for val in self.radioButtonsIn:
            val.configure(state=NORMAL)
        for val in self.radioButtonsOut:
            val.configure(state=NORMAL)
        self.bal = False
        self.unbal = True
        self.canGo()

    def start(self):
        s = Driver_Interop.soundBoard()
        if self.unbal:
            self.createCanvasUnbal()
            self.fun(self.unbalancedCable.channel, 20, 150, 200, 250)
            #Send output over DAC
            #Get input from ADC (set to output)
            s.sendReceiveSamplesUnbal(self.audioSamples, self.unbalIn.get(), self.unbalOut.get(), self.unbalancedCable.sampleRate)
            output = []
            degLvlStr = "Degredation Level: " + str(int(100 * Algos.calculateDifferenceNumber(self.unbalancedCable.channel, output))) + "%"
            self.c.create_text(100, 40, text=degLvlStr)
            self.fun(output, 400, 150, 600, 250)
            self.c.update_idletasks()
            sd.play(output, self.unbalancedCable.sampleRate)
        if self.bal:
            self.balancedCable.changeAudio(self.balChoice)
            self.createCanvasBal()
            out = []
            self.fun(self.audioSamples, 20, 150, 200, 250)
            # Send output over DAC 1 and 2 at same time
            # Get input from ADC 1 and 2 at same time (set to output1 and output2)
            self.balancedCableNoise.channel1, self.balancedCableNoise.channel2 = s.sendReceiveSamplesBal(self.balancedCable.channel1,self.balancedCable.channel2,
                                      self.balancedCable.sampleRate)
            self.fun(self.balancedCableNoise.channel1, 375, 10, 550, 100)
            self.fun(self.balancedCableNoise.channel2, 375, 300, 550, 400)
            finalout = self.balancedCableNoise.differentiate()
            degLvlStr = "Degredation Level: " + str(int(100 * Algos.calculateDifferenceNumber(self.audioSamples, finalout))) + "%"
            self.c.create_text(100, 40, text=degLvlStr)
            self.fun(finalout, 500, 150, 700, 250)
            self.c.update_idletasks()
            sd.play(finalout, self.balancedCableNoise.sampleRate)
        s.closeSoundBoard()
    def stop(self):
        sd.stop()



    def quit(self):
        self.controller.show_frame("Main")

    def introduceNoise(self):
        self.noiseOn = not self.noiseOn

    def fun(self, audio, x0, y0, x1, y1):
        # calculate a random amplitude

        points = []
        for x in range(0, abs(x0 - x1)):
            points.append((x0 + x))
            #points.append(int(y0) + (abs(y0 - y1) / 2 * (audio[x * (int(len(audio)/(abs(x0 - x1))))] + 1) ))
            points.append((int(y0) + (abs(y0 - y1) / 2 * (audio[x] + 1))))
        # now points should be of form [x0, y0, x1, y1, ...]
        # not [(x0, y0), ...]
        self.c.create_line(smooth=1, *points)
          # to draw the shapes immediately.

    def createCanvasUnbal(self):
        for item in self.c.find_all():
            self.c.delete(item)

        self.c.create_line(200,200,400,200)
        self.c.create_line(300, 100, 300, 300)
        self.c.create_rectangle(20,150,200,250, outline='black')
        self.c.create_text(100,260, text="Input")
        self.c.create_rectangle(150, 300, 350, 400, outline='black')
        self.c.create_text(250, 410, text="Noise")
        self.c.create_rectangle(400, 150, 600, 250, outline='black')
        self.c.create_text(500, 260, text="Output")

        self.c.create_text(100, 500, text="Unbalanced Audio Signal")
        #self.c.create_text(100, 40, text="Degredation Level: ")


    def openFile1(self):

        self.file_path1 = filedialog.askopenfilename()
        waveFile = wave.open(self.file_path1, 'r')
        #Use wave to get filename but store information in sf
        file1_info = "Filename: " + str(os.path.basename(self.file_path1)) + "; SampleRate: " + str(waveFile.getframerate()) + "; SampleWidth: " + str(waveFile.getsampwidth())
        self.label1.configure(text=file1_info)
        waveFile.close()

        audio = sf.read(self.file_path1)
        self.balancedCable = balanced(audio)
        self.balancedCableNoise = balanced(audio)
        self.unbalancedCable = unbalanced(audio)
        self.unbalancedCableNoise = unbalanced(audio)
        self.audioSamples = audio[0]



    def createCanvasBal(self):
        for item in self.c.find_all():
            self.c.delete(item)

        self.c.create_line(200, 175, 400, 175)
        self.c.create_line(200, 225, 400, 225)
        #self.c.create_line(250, 100, 250, 300)
        self.c.create_line(450, 200, 500, 200)

        self.c.create_line(425, 150, 425, 100)
        self.c.create_line(425, 250, 425, 300)

        #input
        self.c.create_rectangle(20, 150, 200, 250, outline='black')
        self.c.create_text(100, 260, text="Generated Waveform Section")
        #noise
        #self.c.create_rectangle(150, 300, 350, 400, outline='black')
        #self.c.create_text(250, 410, text="Noise")

        #Chan 1
        self.c.create_rectangle(375, 10, 550, 100, outline='black')
        self.c.create_text(500, 110, text="Channel 1 Return")
        # Chan 2
        self.c.create_rectangle(375, 300, 550, 400, outline='black')
        self.c.create_text(450, 410, text="Channel 2 Return")
        #Diff
        self.c.create_rectangle(400, 150, 450, 250, outline='black')
        self.c.create_text(383, 260, text="Voltage\nDifferentiator")
        #output
        self.c.create_rectangle(500, 150, 700, 250, outline='black')
        self.c.create_text(600, 260, text="Section After VD")

        self.c.create_text(100, 500, text="Balanced Audio Signal")

        #self.c.create_text(100, 40, text="Degredation Level: ")

    def buildSourceList(self, sources):
        i = 2
        for source in sources:
            Radiobutton(self, text=("Source " + str(source)), variable=self.sourceSelection,
                value=source).grid(row = i, column = 1)
            i = i+1
        return i

    def getSources(self):
        # Sources will be populated by the number of outputs in the DAC
        sources = [1, 2, 3, 4, 5]
        return sources

    def buildWavesList(self, waveGenFunctions):
        i = 2
        for funcCount in range(0, len(waveGenFunctions)):
            Radiobutton(self, text=(waveGenFunctions[funcCount]), variable=self.funcSelection,
                value=funcCount).grid(row = i, column = 0)
            i = i+1
        return i

    def getWaves(self):
        # Waveforms can be created in the WaveForms class
        return WaveForms.getFunctions()

    def main(self):
        self.label1 = Label(self, text="No File Selected - 1000Hz Sine Selected")
        Button(self, text='Browse', command=self.openFile1).grid(row=0, column=0)
        self.label1.grid(row=0, column=1)


        #Message(self, text=("Select a waveform")).grid(row=1,column=0)

        #rowCount1 = self.buildWavesList(self.getWaves())
        # Populate sources

        rowCountMax = 2


        Label(self, text="Connector Setup").grid(row=rowCountMax,column=0)
        rowCountMax += 1
        Button(self, text='Balanced (using RCAs 1 and 2)', command=self.setBalanced).grid(row=rowCountMax,column=0)
        self.radioButtons.append(Radiobutton(self, command=self.canGo, text="Carry Signal on RCA 1 Only", variable=self.balChoice, value=1))
        self.radioButtons.append(Radiobutton(self, command=self.canGo, text="Carry Signal on RCA 2 Only", variable=self.balChoice, value=2))
        self.radioButtons.append(Radiobutton(self, command=self.canGo, text="Carry Half Signal on RCA 1 and RCA 2, Reverse RCA 2 Polarity", variable=self.balChoice, value=3))
        i = 0
        for val in self.radioButtons:
            i += 1
            val.configure(state=DISABLED)
            val.grid(row=rowCountMax + i,column=0)


        Button(self, text='Unbalanced', command=self.setUnbalanced).grid(row=rowCountMax,column=1)
        rowCountMax = rowCountMax + 1
        Message(self, text=("Select Input"), width=400).grid(row=rowCountMax, column=1)
        self.radioButtonsIn.append(Radiobutton(self, command=self.canGo, text="RCA 1", variable=self.unbalIn, value=1))
        self.radioButtonsIn.append(Radiobutton(self, command=self.canGo, text="RCA 2", variable=self.unbalIn, value=2))
        i = 0
        for val in self.radioButtonsIn:
            i += 1
            val.configure(state=DISABLED)
            val.grid(row=rowCountMax + i,column=1)
        rowCountMax += i + 1

        Message(self, text=("Select Output"), width=400).grid(row=rowCountMax, column=1)
        self.radioButtonsOut.append(Radiobutton(self, command=self.canGo, text="RCA 1", variable=self.unbalOut, value=1))
        self.radioButtonsOut.append(Radiobutton(self, command=self.canGo, text="RCA 2", variable=self.unbalOut, value=2))
        i = 0
        for val in self.radioButtonsOut:
            i += 1
            val.configure(state=DISABLED)
            val.grid(row=rowCountMax + i,column=1)
        rowCountMax += i + 1

        self.startButton = Button(self, text='Start', state=DISABLED)
        self.stopButton = Button(self, text='Stop', state=DISABLED)
        self.startButton.grid(row=rowCountMax,column=0)
        self.stopButton.grid(row=rowCountMax,column=1)
        rowCountMax += 1
        self.startButton.configure(command=self.start)
        self.stopButton.configure(command=self.stop)
        Button(self, text='Quit', command=self.quit).grid(row=rowCountMax,column=0, columnspan=1)
        rowCountMax += 1

        Label(self, text="Graphical Representation").grid(row=rowCountMax, column=0, columnspan=2)
        self.c = Canvas(self, width=800, height=700, bg='beige')

        self.c.grid(row=rowCountMax,columnspan=2,sticky=W+E)

