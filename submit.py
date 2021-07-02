import os, sys, math
from Scripts import step1, step2, step3, ntuples
from Tools import mainParser, particleNumbers, col

sys.path.append(os.path.abspath(os.path.curdir))

options = mainParser()
particleTags = particleNumbers()

# Getting environment info
cmssw = os.environ['CMSSW_VERSION']
cmsswBase = os.environ['CMSSW_BASE']
user = os.environ['USER']
genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
cwd = os.getcwd()

if __name__ == '__main__':
    if options.step is 'step1':
        step1()
    elif  options.step is 'step2':
        step2()
    elif  options.step is 'step2':
        step3()
    elif  options.step is 'ntuples':
        ntuples()
    else:
        raise ValueError
