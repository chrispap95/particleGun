import os, sys

# Getting environment info
cmssw = os.environ['CMSSW_VERSION']
cmsswBase = os.environ['CMSSW_BASE']
user = os.environ['USER']
genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
cwd = os.getcwd()

def step2():
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
            eTag = '%sto%s'%(minEnTag,maxEnTag)
        else:
            eTag = '%s %d'%(eTag,E)
    pTag = ''
    for p in particles:
        pTag = '%s %d'%(pTag,p)
    etaList = ''
    for etaTag in etaTags:
        if etaTag == 'notSet':
            etaList = '%sto%s'%(minEtaTag,maxEtaTag)
        else:
            etaList = '%s %s'%(etaList,etaTag)
    phiList = ''
    for phiTag in phiTags:
        if phiTag == 'notSet':
            if options.minPhi is not None or options.maxPhi is not None:
                phiList = '%sto%s'%(minPhiTag,maxPhiTag)
        else:
            phiList = '%s %s'%(phiList,phiTag)
    os.system("sh Tools/createList.sh step1 '%s' '%s' '%s' '%s' '%s' '%s' '%s' "
    "'%s' "%(eTag,pTag,options.geometry,etaList,phiList,options.inputTag,options.closeBy,options.campaign))
    filein = open('myGeneration/list.txt','r')

    for p in particles:
        for E in energies:
            for etaTag in etaTags:
                for phiTag in phiTags:
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
