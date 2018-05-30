def getFunctions():
    return list(filter(lambda x: "_" not in x, dir(waveFunctions)))

def funcExists (funcName):
        return funcName in dir(waveFunctions)

def callFunc (funcName):
    if funcExists(funcName):
        getattr(waveFunctions, funcName)
    else:
        raise NameError('Invalid function name')

class waveFunctions:
    def sine(self):
        return False

    def square(self):
        return False

    def saw(self):
        return False

    def userWave(self):
        return False
