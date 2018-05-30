import wave
import soundfile as sf
import sounddevice as sd

def calculateDifference(array1, array2, accuracy = 1):
    array3 = [0] * len(array1)
    for i in range (0, len(array1), accuracy):
        val = array1[i] - array2[i]
        array3[i] = val
    return array3


def calculateDifferenceNumber(array1, array2, accuracy = 1):
    difference = 0
    for i in range (0, len(array1), accuracy):
        val = abs(array1[i]) - abs(array2[i])
        difference += abs (val)
    difference /= (len(array1) / accuracy)
    return difference

def genWaveFromArray(array1):
    array3 = [0] * len(array1)
    samples1, samplerate1 = sf.read("sin_900Hz.wav")
    samples2, samplerate2 = sf.read("sin_1000Hz.wav")
    for i in range(0, len(samples1)):
        array3[i] = abs(samples1[i] - samples2[i])
    sd.play(array3, samplerate1)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)