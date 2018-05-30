driverInstalled = False
haveRoot = False
import os
if os.geteuid() == 0:
    haveRoot = True
    try:
        import audioInterop
        driverInstalled = True
    except:
        driverInstalled = False
else:
    print("Error, no root, driver disabled")


import time

class soundBoard():
    inputs = [int]
    outputs = [int]
    #Initialize Board and
    def __init__(self):
        if driverInstalled:
            try:
                audioInterop.myInitFunction()
                self.connected = True
            except:
                self.connected = False

            self.t = time.time()

    def sendReceiveSamplesBal(self, sample1, sample2, sampleRate):
        channels = audioInterop.myMainFunctionBal(float(sampleRate), sample1, sample2)
        channel1 = channels[0]
        channel2 = channels[1]
        return channel1, channel2

    def sendReceiveSamplesUnbal(self, sample, inChoice, outChoice, sampleRate):
        samples = audioInterop.myMainFunctionUnbal(inChoice, outChoice, float(sampleRate), sample)
        
        return samples
            
            
    def closeSoundBoard(self):
        audioInterop.myClosingFunction()
        print("\nClosed AudioBoard\n")

def checkSoundboard():
    if driverInstalled:
        try:
            audioInterop.myInitFunction()
            audioInterop.myClosingFunction()
            return True
        except:
            return False
    else:
        return False

#print(checkSoundboard())
#s = soundBoard()
#samples = []

#samples = s.sendReceiveSamplesUnbal(([1.0] * 100),1,2,500)
#channel1, channel2 = s.sendReceiveSamplesBal(([1.0] * 100),([2.0] * 100),500)
#print("Chan1: " + str(channel1))
#print("Chan2: " + str(channel2))

