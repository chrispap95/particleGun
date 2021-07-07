import os, sys, math
from Tools import particleNumbers, col, makeTag, tagBuilder, writeCRABConfig

def step3(options):
    # Getting environment info
    CMSSW = os.environ['CMSSW_VERSION']
    USER = os.environ['USER']
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
        print('%sWarning%s: Particles not specified. Using Gamma as default. '
        'This might not be compatible with your configuration.'%(col.magenta,col.endc))
        particles = [22]

    # Get memory, maxTime and numCores configuration
    maxRuntime = 50
    if options.maxRuntime is not None:
        maxRuntime = options.maxRuntime
    memory = 5000
    if options.memory is not None:
        memory = options.memory
    nThreads = 4
    if options.cpu is not None:
        nThreads = options.cpu

    # Pileup configuration
    pileupInput = ''
    pileupConfig = ''
    if options.pileup:
        if options.cpu is None:
            nThreads = 8
        if options.memory is None:
            nThreads = 16000
        pileupInput = '--pileup_input das:/RelValMinBias_14TeV/CMSSW_11_3_0_pre3-113X_mcRun4_realistic_v3_2026D76noPU-v1/GEN-SIM'
        pileupConfig = '--pileup AVE_200_BX_25ns'

    # Run cmsdriver.py to create workflows
    print('Creating step3 configuration.')
    os.system('cmsDriver.py step3 --conditions auto:%s -n 100 %s %s --era %s '
    '--eventcontent FEVTDEBUGHLT --no_exec -s RAW2DIGI,L1Reco,RECO,RECOSIM --mc '
    '--datatier GEN-SIM-RECO --geometry Extended2026%s --nThreads %d --filein file:step2.root '
    '--fileout file:step3.root'%(options.conditions, pileupInput, pileupConfig, options.era, options.geometry, nThreads))
    script = 'step3_RAW2DIGI_L1Reco_RECO_RECOSIM.py'
    if options.pileup:
        script = 'step3_RAW2DIGI_L1Reco_RECO_RECOSIM_PU.py'

    # Get filenames from previous step
    eTag = ''
    for E in energies:
        if E == 'notSet':
            eTag = '%sto%s'%(makeTag(minEn),makeTag(maxEn))
        else:
            eTag = '%s %s'%(eTag,makeTag(E))
    pTag = ''
    for p in particles:
        pTag = '%s %d'%(pTag,p)
    etaList = ''
    for eta in etas:
        if eta == 'notSet':
            etaList = '%sto%s'%(makeTag(minEta),makeTag(maxEta))
        else:
            etaList = '%s %s'%(etaList,makeTag(eta))
    phiList = ''
    for phi in phis:
        if phi == 'notSet':
            if options.minPhi is not None or options.maxPhi is not None:
                phiList = '%sto%s'%(makeTag(minPhi),makeTag(maxPhi))
        else:
            phiList = '%s %s'%(phiList,makeTag(phi))
    inputTag = options.inputTag
    if options.inputTag is None:
        inputTag = options.tag
    os.system("sh Tools/createList.sh step2 '%s' '%s' '%s' '%s' '%s' '%s' '%s' "
    "'%s' "%(eTag,pTag,options.geometry,etaList,phiList,inputTag,options.closeBy,options.campaign))
    filein = open('myGeneration/list.txt','r')

    for p in particles:
        for E in energies:
            for eta in etas:
                for phi in phis:
                    # Append particle, energy, eta and phi tags. Phi tag is skipped if full range is used
                    # and create printout message.
                    outTag = tagBuilder(options, p, E, eta, phi, minEn, maxEn, minEta, maxEta, minPhi, maxPhi)

                    os.chdir(CWD)
                    os.system('cp %s myGeneration/%s/'%(script,outTag))
                    os.chdir('myGeneration/%s'%outTag)

                    # Create CRAB configuration file
                    writeCRABConfig(options, outTag, nThreads, memory, maxRuntime, filein, CMSSW, USER, script)

                    if options.no_exec:
                        os.system('crab submit -c crabConfig_%s_step3.py'%outTag)

    os.chdir(CWD)
    os.system('rm %s'%script)
