import os, sys
from Tools import mainParser, particleNumbers, col

sys.path.append(os.path.abspath(os.path.curdir))

options = mainParser()
particleTags = particleNumbers()

if __name__ == '__main__':
    # List or range of energies to shoot particles
    minEnTag, maxEnTag = '0', '650'
    if options.maxEn is not None:
        maxEnTag = options.maxEn
        maxEn = float(options.maxEn.replace("p","."))
    if options.minEn is not None:
        minEnTag = options.minEn
        minEn = float(options.minEn.replace("p","."))
    energies = options.energies
    if energies is None or len(energies) == 0:
        energies = ['notSet']

    # List or range of etas to shoot particles
    minEtaTag, maxEtaTag = '1p5', '3p0'
    if options.maxEta is not None:
        maxEtaTag = options.maxEta.replace("-","minus")
        maxEta = float(options.maxEta.replace("p","."))
    if options.minEta is not None:
        minEtaTag = options.minEta.replace("-","minus")
        minEta = float(options.minEta.replace("p","."))
    etaTags = options.eta
    if etaTags is None or len(etaTags) == 0:
        etaTags = ['notSet']

    # List or range of phi to shoot particles
    minPhiTag, maxPhiTag = 'minusPi', 'Pi'
    if options.maxPhi is not None:
        maxPhiTag = options.maxPhi.replace("-","minus")
        maxPhi = float(options.maxPhi.replace("p","."))
    if options.minPhi is not None:
        minPhiTag = options.minPhi.replace("-","minus")
        minPhi = float(options.minPhi.replace("p","."))
    phiTags = options.phi
    if phiTags is None or len(phiTags) == 0:
        phiTags = ['notSet']

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
                    # Append particle, energy, eta and phi tags. Phi tag is skipped if full range is used
                    # and create printout message.
                    outTag = ''
                    printOut = '%s%s'%(col.bold, col.green)
                    if options.closeBy:
                        outTag = 'CloseBy'
                        printOut = 'Using CloseBy gun.\n'
                    particleTag = particleTags[p]
                    outTag = '%sSingle%s'%(outTag,particleTag)
                    printOut = '%sResubmitting jobs for %s with '%(printOut,particleTag)
                    if E == 'notSet':
                        outTag = '%s_E%sto%s'%(outTag,minEnTag,maxEnTag)
                        printOut = '%sE in (%s,%s) GeV, '%(printOut,minEnTag,maxEnTag)
                    else:
                        outTag = '%s_E%d'%(outTag,E)
                        printOut = '%sE=%d GeV, '%(printOut,E)
                    if etaTag == 'notSet':
                        outTag = '%sEta%sto%s'%(outTag,minEtaTag,maxEtaTag)
                        printOut = '%seta in (%s,%s), '%(printOut,minEtaTag,maxEtaTag)
                    else:
                        outTag = '%sEta%s'%(outTag,etaTag)
                        printOut = '%seta=%s, '%(printOut,etaTag)
                    if phiTag == 'notSet':
                        if options.minPhi is not None or options.maxPhi is not None:
                            outTag = '%sPhi%sto%s'%(outTag,minPhiTag,maxPhiTag)
                        printOut = '%sand phi in (%s,%s)%s'%(printOut,minPhiTag,maxPhiTag,col.endc)
                    else:
                        outTag = '%sPhi%s'%(outTag,phiTag)
                        printOut = '%sand phi=%s%s'%(printOut,phiTag,col.endc)
                    print(printOut)
                    print('%sCampaign: %s%s%s\t%sTag: %s%s%s'%(col.bold,col.magenta,options.campaign,col.endc,
                                                               col.bold,col.magenta,options.tag,col.endc))
                    os.chdir(cwd)
                    os.chdir('myGeneration/%s/crab_projects/'%outTag)
                    if options.campaign is None:
                        if options.tag is None:
                            os.system('ls | grep %s | grep %s '
                            '> submissions.txt'%(options.step,options.geometry))
                        else:
                            os.system('ls | grep %s | grep %s | grep %s '
                            '> submissions.txt'%(options.step,options.geometry,options.tag))
                    else:
                        if options.tag is None:
                            os.system('ls | grep %s | grep %s | grep %s '
                            '> submissions.txt'%(options.step,options.geometry,options.campaign))
                        else:
                            os.system('ls | grep %s | grep %s | grep %s | grep %s '
                            '> submissions.txt'%(options.step,options.geometry,options.tag,options.campaign))
                    fSubmissions = open('submissions.txt','r')
                    for submission in fSubmissions:
                        os.system('crab resubmit --siteblacklist=T2_US_Caltech -d %s'%(submission))
                    os.system('rm submissions.txt')
