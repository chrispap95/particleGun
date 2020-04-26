import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

from Tools import standardParser, particleNumbers, col
options = standardParser()
particleTags = particleNumbers()

if __name__ == '__main__':
    # List of energies to shoot
    energies = options.energies
    if energies is None or len(energies) == 0:
        print(col.magenta+'Warning:'+col.endc+'Energies not specified. '
        'Using default values that might not work in your case.')
        energies = [1,3,5,10,15,20,25,30]

    # List of etas to shoot particles
    etaTags = options.eta
    if etaTags is None or len(etaTags) == 0:
        print(col.magenta+'Warning: '+col.endc+'Etas not specified. '
        'Using default values that might not work in your case.')
        etaTags = ['1p7']
    etas = {}
    for etaTag in etaTags:
        etas[etaTag] = float(etaTag.replace("p","."))

    # List of phi to shoot particles
    phiTags = options.phi
    if phiTags is None or len(phiTags) == 0:
        print(col.magenta+'Warning: '+col.endc+'Phi not specified. '
        'The script is not going to specify a Phi.')
        phiTags = ['notSet']
    phis = {}
    for phiTag in phiTags:
        if phiTag != 'notSet':
            phis[phiTag] = float(phiTag.replace("p","."))

    # List of particles to generate in pdg codes
    particles = options.particles
    if particles is None or len(particles) == 0:
        print(col.magenta+'Warning: '+col.endc+'Particles not specified. '
        'Using Gamma as default. This might not be compatible with your configuration.')
        particles = [22]

    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

    for p in particles:
        for E in energies:
            for etaTag in etaTags:
                for phiTag in phiTags:
                    particleTag = particleTags[p]
                    outTag = 'Single%s'%particleTag
                    outTag = '%s_E%d'%(outTag,E)
                    outTag = '%sEta%s'%(outTag,etaTag)
                    if phiTag != 'notSet':
                        outTag = '%sPhi%s'%(outTag,phiTag)
                    if phiTag != 'notSet':
                        print('%sChecking%s status for %s at E=%d Eta=%s Phi=%s.'%(col.yellow,col.endc,particleTag,E,etaTag,phiTag))
                    else:
                        print('%sChecking%s status for %s at E=%d Eta=%s.'%(col.yellow,col.endc,particleTag,E,etaTag))
                    os.chdir(cwd)
                    os.chdir('myGeneration/%s/crab_projects/'%outTag)
                    if options.tag is None or options.tag == None:
                        os.system('ls | grep %s | grep %s '
                        '> submissions.txt'%(options.step,options.geometry))
                    else:
                        os.system('ls | grep %s | grep %s | grep %s '
                        '> submissions.txt'%(options.step,options.geometry,options.tag))
                    fSubmissions = open('submissions.txt','r')
                    for submission in fSubmissions:
                        os.system('crab status -d %s > log.txt'%(submission))
                        os.system('tail -n +9 log.txt | head -n -8')
                        os.system('rm log.txt')
                    os.system('rm submissions.txt')
