import os, sys, math
from Scripts import step1, step2, step3, ntuples
from Tools import mainParser, particleNumbers, col

sys.path.append(os.path.abspath(os.path.curdir))

options = mainParser()
particleTags = particleNumbers()

if __name__ == '__main__':
    if options.step == 'step1':
        step1.step1()
    elif  options.step == 'step2':
        step2.step2()
    elif  options.step == 'step2':
        step3.step3()
    elif  options.step == 'ntuples':
        ntuples.ntuples()
    else:
        raise ValueError
