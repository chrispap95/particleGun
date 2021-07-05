import os, sys, math
from Tools import particleNumbers, col

def step2(options):
    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    user = os.environ['USER']
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
        'Using Gamma as default. This might not be compatible with your configuration.\n')
        particles = [22]

    # Pileup configuration
    pileupInput = ''
    pileupConfig = ''
    nThreads = '4'
    if options.pileup:
        pileupInput = '--pileup_input das:/RelValMinBias_14TeV/CMSSW_11_3_0_pre3-113X_mcRun4_realistic_v3_2026D76noPU-v1/GEN-SIM'
        pileupConfig = '--pileup AVE_200_BX_25ns'

    if options.cpu is not None:
        nThreads = options.cpu

    # Run cmsdriver.py to create workflows
    print('Creating step2 configuration.')
    os.system('cmsDriver.py step2 --mc '
    '-s DIGI:pdigi_valid,L1TrackTrigger,L1,DIGI2RAW,HLT:@fake2 --nThreads %s '
    '--datatier GEN-SIM-DIGI-RAW -n 100 --geometry Extended2026%s %s %s --era %s '
    '--eventcontent FEVTDEBUGHLT --no_exec --conditions auto:%s --filein file:step1.root '
    '--fileout file:step2.root'%(nThreads, options.geometry, pileupInput, pileupConfig, options.era, options.conditions))

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
        inputTag = options.Tag
    os.system("sh Tools/createList.sh step1 '%s' '%s' '%s' '%s' '%s' '%s' '%s' "
    "'%s' "%(eTag,pTag,options.geometry,etaList,phiList,inputTag,options.closeBy,options.campaign))
    filein = open('myGeneration/list.txt','r')

    for p in particles:
        for E in energies:
            for eta in etas:
                for phi in phis:
                    # Append particle, energy, eta and phi tags. Phi tag is skipped if full range is used
                    # and create printout message.
                    outTag = ''
                    printOut = '%s%s'%(col.bold, col.yellow)
                    if options.closeBy:
                        outTag = 'CloseBy'
                        printOut = 'Using CloseBy gun.\n'
                    particleTag = particleTags[p]
                    outTag = '%sSingle%s'%(outTag,particleTag)
                    printOut = '%sCreating configuration for %s with '%(printOut,particleTag)
                    if E == 'notSet':
                        outTag = '%s_E%sto%s'%(outTag,makeTag(minEn),makeTag(maxEn))
                        printOut = '%sE in (%s,%s) GeV, '%(printOut,makeTag(minEn),makeTag(maxEn))
                    else:
                        outTag = '%s_E%d'%(outTag,makeTag(E))
                        printOut = '%sE=%d GeV, '%(printOut,makeTag(E))
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

                    os.chdir(cwd)
                    if options.pileup:
                        os.system('cp step2_DIGI_L1TrackTrigger_L1_DIGI2RAW_HLT_PU.py myGeneration/%s/'%outTag)
                    else:
                        os.system('cp step2_DIGI_L1TrackTrigger_L1_DIGI2RAW_HLT.py myGeneration/%s/'%outTag)
                    os.chdir('myGeneration/%s'%outTag)

                    # Create CRAB configuration file
                    file1 = open('crabConfig_%s_step2.py'%outTag,'w')
                    file1.write('# Script automatically generated by step2.py\n\n')

                    file1.write('from CRABClient.UserUtilities ')
                    file1.write('import config\n')
                    file1.write('config = config()\n')
                    file1.write("config.General.requestName = ")
                    if options.campaign is None:
                        if options.tag is None:
                            file1.write("'%s_%s_upgrade2026_%s_step2'\n"%(outTag,cmssw,options.geometry))
                        else:
                            file1.write("'%s_%s_upgrade2026_%s_%s_step2'\n"%(outTag,cmssw,options.geometry,options.tag))
                    else:
                        if options.tag is None:
                            file1.write("'%s_%s_upgrade2026_%s_%s_step2'\n"%(outTag,cmssw,options.geometry,options.campaign))
                        else:
                            file1.write("'%s_%s_upgrade2026_%s_%s_%s_step2'\n"%(outTag,cmssw,options.geometry,options.campaign,options.tag))
                    file1.write("config.General.workArea = 'crab_projects'\n")
                    file1.write("config.General.transferOutputs = True\n")
                    file1.write("config.General.transferLogs = True\n\n")

                    file1.write("config.JobType.pluginName = 'Analysis'\n")
                    file1.write("config.JobType.psetName = ")
                    if options.pileup:
                        file1.write("'step2_DIGI_L1TrackTrigger_L1_DIGI2RAW_HLT_PU.py'\n")
                    else:
                        file1.write("'step2_DIGI_L1TrackTrigger_L1_DIGI2RAW_HLT.py'\n")
                    if options.memory is None:
                        file1.write("config.JobType.maxMemoryMB = 5000\n")
                    else:
                        file1.write("config.JobType.maxMemoryMB = %s\n"%options.memory)
                    file1.write("config.JobType.numCores = %s\n"%nThreads)
                    file1.write("config.JobType.maxJobRuntimeMin = 60\n\n")

                    file1.write("config.Data.inputDataset = '%s'\n"%((filein.readline())[:-1]))
                    file1.write("config.Data.inputDBS = 'phys03'\n")
                    file1.write("config.Data.splitting = 'FileBased'\n")
                    file1.write("config.Data.unitsPerJob = %d\n"%options.unitsPerJob)
                    file1.write("config.Data.totalUnits = %d\n"%options.njobs)
                    file1.write("config.Data.outLFNDirBase = '%s%s/'\n"%(options.dest,user))
                    file1.write("config.Data.publication = True\n")
                    file1.write("config.Data.outputDatasetTag = ")
                    if options.campaign is None:
                        file1.write("'%s_%s_upgrade2026_%s_step2'\n\n"%(outTag,cmssw,options.geometry))
                    else:
                        file1.write("'%s_%s_upgrade2026_%s_%s_step2'\n\n"%(outTag,cmssw,options.geometry,options.campaign))

                    file1.write("config.Site.storageSite = '%s'\n"%options.site)
                    file1.write("config.Site.blacklist = ['T2_US_Caltech']\n")
                    file1.close()

                    if options.no_exec:
                        os.system('crab submit -c crabConfig_%s_step2.py'%outTag)

    os.chdir(cwd)
    if options.pileup:
        os.system('rm step2_DIGI_L1TrackTrigger_L1_DIGI2RAW_HLT_PU.py')
    else:
        os.system('rm step2_DIGI_L1TrackTrigger_L1_DIGI2RAW_HLT.py')
