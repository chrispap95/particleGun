import os, sys, math
from Tools import particleNumbers, col, makeTag, tagBuilder

def step3(options):
    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    user = os.environ['USER']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

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

    # Pileup configuration
    pileupInput = ''
    pileupConfig = ''
    nThreads = '4'
    if options.pileup:
        pileupInput = '--pileup_input das:/RelValMinBias_14TeV/CMSSW_11_3_0_pre3-113X_mcRun4_realistic_v3_2026D76noPU-v1/GEN-SIM'
        pileupConfig = '--pileup AVE_200_BX_25ns'
        nThreads = '8'

    if options.cpu is not None:
        nThreads = options.cpu

    # Run cmsdriver.py to create workflows
    print('Creating step3 configuration.')
    os.system('cmsDriver.py step3 --conditions auto:%s -n 100 %s %s --era %s '
    '--eventcontent FEVTDEBUGHLT --no_exec -s RAW2DIGI,L1Reco,RECO,RECOSIM --mc '
    '--datatier GEN-SIM-RECO --geometry Extended2026%s --nThreads %s --filein file:step2.root '
    '--fileout file:step3.root'%(options.conditions, pileupInput, pileupConfig, options.era, options.geometry, nThreads))

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
    os.system("sh Tools/createList.sh step2 '%s' '%s' '%s' '%s' '%s' '%s' '%s' "
    "'%s' "%(eTag,pTag,options.geometry,etaList,phiList,inputTag,options.closeBy,options.campaign))
    filein = open('myGeneration/list.txt','r')

    for p in particles:
        for E in energies:
            for eta in etas:
                for phi in phis:
                    # Append particle, energy, eta and phi tags. Phi tag is skipped if full range is used
                    # and create printout message.
                    outTag = tagBuilder(options, p, E, eta, phi)

                    os.chdir(cwd)
                    if options.pileup:
                        os.system('cp step3_RAW2DIGI_L1Reco_RECO_RECOSIM_PU.py myGeneration/%s/'%outTag)
                    else:
                        os.system('cp step3_RAW2DIGI_L1Reco_RECO_RECOSIM.py myGeneration/%s/'%outTag)
                    os.chdir('myGeneration/%s'%outTag)

                    # Create CRAB configuration file
                    file1 = open('crabConfig_%s_step3.py'%outTag,'w')
                    file1.write('# Script automatically generated using generator.py\n\n')

                    file1.write('from CRABClient.UserUtilities ')
                    file1.write('import config\n')
                    file1.write('config = config()\n')
                    file1.write("config.General.requestName = ")
                    if options.campaign is None:
                        if options.tag is None:
                            file1.write("'%s_%s_upgrade2026_%s_step3'\n"%(outTag,cmssw,options.geometry))
                        else:
                            file1.write("'%s_%s_upgrade2026_%s_%s_step3'\n"%(outTag,cmssw,options.geometry,options.tag))
                    else:
                        if options.tag is None:
                            file1.write("'%s_%s_upgrade2026_%s_%s_step3'\n"%(outTag,cmssw,options.geometry,options.campaign))
                        else:
                            file1.write("'%s_%s_upgrade2026_%s_%s_%s_step3'\n"%(outTag,cmssw,options.geometry,options.campaign,options.tag))
                    file1.write("config.General.workArea = 'crab_projects'\n")
                    file1.write("config.General.transferOutputs = True\n")
                    file1.write("config.General.transferLogs = True\n\n")

                    file1.write("config.JobType.pluginName = 'Analysis'\n")
                    file1.write("config.JobType.psetName = ")
                    if options.pileup:
                        file1.write("'step3_RAW2DIGI_L1Reco_RECO_RECOSIM_PU.py'\n")
                        if options.memory is None:
                            file1.write("config.JobType.maxMemoryMB = 16000\n")
                        else:
                            file1.write("config.JobType.maxMemoryMB = %s\n"%options.memory)
                    else:
                        file1.write("'step3_RAW2DIGI_L1Reco_RECO_RECOSIM.py'\n")
                        if options.memory is None:
                            file1.write("config.JobType.maxMemoryMB = 5000\n")
                        else:
                            file1.write("config.JobType.maxMemoryMB = %s\n"%options.memory)
                    file1.write("config.JobType.numCores = %s\n"%nThreads)
                    file1.write("config.JobType.maxJobRuntimeMin = 50\n\n")

                    file1.write("config.Data.inputDataset = '%s'\n"%((filein.readline())[:-1]))
                    file1.write("config.Data.inputDBS = 'phys03'\n")
                    file1.write("config.Data.splitting = 'FileBased'\n")
                    file1.write("config.Data.unitsPerJob = %d\n"%options.unitsPerJob)
                    file1.write("config.Data.totalUnits = %d\n"%options.njobs)
                    file1.write("config.Data.outLFNDirBase = '%s%s/'\n"%(options.dest,user))
                    file1.write("config.Data.publication = True\n")
                    file1.write("config.Data.outputDatasetTag = ")
                    if options.campaign is None:
                        file1.write("'%s_%s_upgrade2026_%s_step3'\n\n"%(outTag,cmssw,options.geometry))
                    else:
                        file1.write("'%s_%s_upgrade2026_%s_%s_step3'\n\n"%(outTag,cmssw,options.geometry,options.campaign))

                    file1.write("config.Site.storageSite = '%s'\n"%options.site)
                    file1.write("config.Site.blacklist = ['T2_US_Caltech']\n")
                    file1.close()

                    if options.no_exec:
                        os.system('crab submit -c crabConfig_%s_step3.py'%outTag)

    os.chdir(cwd)
    if options.pileup:
        os.system('rm step3_RAW2DIGI_L1Reco_RECO_RECOSIM_PU.py')
    else:
        os.system('rm step3_RAW2DIGI_L1Reco_RECO_RECOSIM.py')
