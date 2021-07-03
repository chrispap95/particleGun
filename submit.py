import os, sys
from Scripts import step1, step2, step3, ntuples
from Tools import mainParser

sys.path.append(os.path.abspath(os.path.curdir))

options = mainParser()

if __name__ == '__main__':
    if options.step == 'step1':
        step1.step1(options)
    elif  options.step == 'step2':
        step2.step2(options)
    elif  options.step == 'step3':
        step3.step3(options)
    elif  options.step == 'ntuples':
        ntuples.ntuples(options)
    else:
        raise ValueError("Unknown step '%s'"%options.step)
