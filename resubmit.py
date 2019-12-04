import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

from Tools import standardParser, particleNumbers
options = standardParser()
particleDict = particleNumbers()

if __name__ == '__main__':
    energies = [1,3,5,10,15,20,25,30] # List of energies of generated particles
    etaTags = ['1p7']                 # List of etas to shoot particles
    etas = {}
    etas['1p7'] = 1.7
    particles = [130]                 # List of particles to generate in pdg codes
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

    for p in particles:
        for E in energies:
            for etaTag in etaTags:
                outTag = 'SingleK0L'
                outTag = '%s_E%d'%(outTag,E)
                outTag = '%sEta%s'%(outTag,etaTag)
                print('Resubmitting failed jobs for K0L at E=%d Eta=%s.'%(E,etaTag))
		os.system('crab resubmit -d myGeneration/%s/crab_projects/crab_%s_%s'
		'_upgrade2023_%s_%s'%(outTag,outTag,cmssw,options.geometry,options.step))

