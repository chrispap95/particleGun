import os, sys, math
from Tools import mainParser, particleNumbers, col, makeTag, tagBuilder

sys.path.append(os.path.abspath(os.path.curdir))

options = mainParser()

if __name__ == '__main__':
    # Getting environment info
    CWD = os.getcwd()

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
                    outTag = tagBuilder(options, p, E, eta, phi, minEn, maxEn, minEta, maxEta, minPhi, maxPhi)
                    print('%sCampaign: %s%s%s\t%sTag: %s%s%s'%(col.bold,col.magenta,options.campaign,col.endc,
                                                               col.bold,col.magenta,options.tag,col.endc))
                    os.chdir(CWD)
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
                        os.system('crab status -d %s > log.txt'%(submission))
                        os.system('tail -n +9 log.txt | head -n -8')
                        os.system('rm log.txt')
                    os.system('rm submissions.txt')
