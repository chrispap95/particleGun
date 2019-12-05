import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

from Tools import standardParser, particleNumbers
options = standardParser()
particleTags = particleNumbers()

if __name__ == '__main__':
    # List of energies to shoot
    energies = options.energies
    if energies is None or len(energies) == 0:
	print('Energies not specified. '
    'Using default values that might not work in your case.')
        energies = [1,3,5,10,15,20,25,30]

    # List of etas to shoot particles
    etaTags = ['1p7']
    etas = {}
    etas['1p7'] = 1.7

    # List of particles to generate in pdg codes
    particles = options.particles
    if particles is None or len(particles) == 0:
	print('Particles not specified. Using Gamma as default. '
    'This might not be compatible with your configuration.')
        particles = [22]

    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

    for p in particles:
        for E in energies:
            for etaTag in etaTags:
		particleTag = particleTags[p]
                outTag = 'Single%s'%particleTag
                outTag = '%s_E%d'%(outTag,E)
                outTag = '%sEta%s'%(outTag,etaTag)
                print('Checking status for K0L at E=%d Eta=%s.'%(E,etaTag))
		os.system('crab status -d myGeneration/%s/crab_projects/crab_%s_%s_'
        'upgrade2023_%s_%s > log.txt'%(outTag,outTag,cmssw,options.geometry,options.step))
		os.system('tail -n +9 log.txt | head -n -8')
		os.system('rm log.txt')
