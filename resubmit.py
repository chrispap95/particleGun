import os, sys, math
from Tools import mainParser, particleNumbers, col

sys.path.append(os.path.abspath(os.path.curdir))

options = mainParser()

if __name__ == '__main__':
    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

    # Converts floats to nice strings for printouts and names
    makeTag = lambda x : str(round(x,2)).replace(".","p").replace("-","minus")

    # List or range of energies to shoot particles
    minEn, maxEn = 0, 650
    if options.maxEn is not None:
        maxEn = options.maxEn
    if options.minEn is not None:
        minEn = options.minEn
    energies = options.energies
    if energies is None or len(energies) == 0:
        energies = ['notSet']

    # List or range of etas to shoot particles
    minEta, maxEta = 1.5, 3.0
    if options.maxEta is not None:
        maxEta = options.maxEta
    if options.minEta is not None:
        minEta = options.minEta
    etas = options.eta
    if etas is None or len(etas) == 0:
        etas = ['notSet']

    # List or range of phi to shoot particles
    minPhi, maxPhi = -math.pi, math.pi
    if options.maxPhi is not None:
        maxPhi = options.maxPhi
    if options.minPhi is not None:
        minPhi = options.minPhi
    phis = options.phi
    if phis is None or len(phis) == 0:
        phis = ['notSet']

    # List of particles to generate in pdg codes
    particleTags = particleNumbers()
    particles = options.particles
    if particles is None or len(particles) == 0:
        print(col.magenta+'Warning: '+col.endc+'Particles not specified. '
        'Using Gamma as default. This might not be compatible with your configuration.')
        particles = [22]

    for p in particles:
        for E in energies:
            for eta in etas:
                for phi in phis:
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
                        outTag = '%s_E%sto%s'%(outTag,makeTag(minEn),makeTag(maxEn))
                        printOut = '%sE in (%s,%s) GeV, '%(printOut,makeTag(minEn),makeTag(maxEn))
                    else:
                        outTag = '%s_E%s'%(outTag,makeTag(E))
                        printOut = '%sE=%s GeV, '%(printOut,makeTag(E))
                    if eta == 'notSet':
                        outTag = '%sEta%sto%s'%(outTag,makeTag(minEta),makeTag(maxEta))
                        printOut = '%seta in (%s,%s), '%(printOut,makeTag(minEta),makeTag(maxEta))
                    else:
                        outTag = '%sEta%s'%(outTag,makeTag(eta))
                        printOut = '%seta=%s, '%(printOut,makeTag(eta))
                    if phi == 'notSet':
                        if options.minPhi is not None or options.maxPhi is not None:
                            outTag = '%sPhi%sto%s'%(outTag,makeTag(minPhi),makeTag(maxPhi))
                        printOut = '%sand phi in (%s,%s)%s'%(printOut,makeTag(minPhi),makeTag(maxPhi),col.endc)
                    else:
                        outTag = '%sPhi%s'%(outTag,makeTag(phi))
                        printOut = '%sand phi=%s%s'%(printOut,makeTag(phi),col.endc)
                    print(printOut)
                    print('%sCampaign: %s%s%s\t%sTag: %s%s%s'%(col.bold,col.magenta,options.campaign,col.endc,
                                                               col.bold,col.magenta,options.tag,col.endc))
                    os.chdir(cwd)
                    os.chdir('myGeneration/%s/crab_projects/'%outTag)

                    listCommand = 'ls | grep %s | grep %s'%(options.step,options.geometry)
                    if options.campaign is not None:
                        listCommand  = '%s| grep %s '%(listCommand,options.campaign)
                    if options.tag is not None:
                        listCommand  = '%s| grep %s '%(listCommand,options.tag)
                    listCommand = '%s> submissions.txt'%(listCommand)
                    os.system(listCommand)

                    fSubmissions = open('submissions.txt','r')
                    for submission in fSubmissions:
                        os.system('crab resubmit --siteblacklist=T2_US_Caltech -d %s'%(submission))
                    os.system('rm submissions.txt')
