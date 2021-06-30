import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

from Tools import mainParserStepN, particleNumbers, col
options = mainParserStepN()
particleTags = particleNumbers()

if __name__ == '__main__':
    # List of energies to shoot
    energies = options.energies
    if energies is None or len(energies) == 0:
        print(col.magenta+'Warning: '+col.endc+'Energies not specified. '
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
        'Using Gamma as default. This might not be compatible with your configuration.\n')
        particles = [22]

    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    user = os.environ['USER']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

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
    os.system('cmsDriver.py step2 '
    '-s DIGI:pdigi_valid,L1TrackTrigger,L1,DIGI2RAW,HLT:@fake2 --nThreads %s '
    '--datatier GEN-SIM-DIGI-RAW -n 100 --geometry Extended2026%s %s %s --era %s '
    '--eventcontent FEVTDEBUGHLT --no_exec --conditions auto:%s --filein file:step1.root '
    '--fileout file:step2.root'%(options.cpu, options.geometry, pileupInput, pileupConfig, options.era, options.conditions))

    # Get filenames from previous step
    eTag = ''
    for E in energies:
        eTag = '%s %d'%(eTag,E)
    pTag = ''
    for p in particles:
        pTag = '%s %d'%(pTag,p)
    etaList = ''
    for etaTag in etaTags:
        etaList = '%s %s'%(etaList,etaTag)
    phiList = ''
    for phiTag in phiTags:
        if phiTag != 'notSet':
            phiList = '%s %s'%(phiList,phiTag)
    os.system("sh createList.sh step1 '%s' '%s' '%s' '%s' '%s' '%s' '%s' "
    "'%s' "%(eTag,pTag,options.geometry,etaList,phiList,options.inputTag,options.closeBy,options.campaign))
    filein = open('myGeneration/list.txt','r')

    for p in particles:
        for E in energies:
            for etaTag in etaTags:
                for phiTag in phiTags:
                    outTag = ''
                    if options.closeBy:
                        outTag = 'CloseBy'
                    particleTag = particleTags[p]
                    outTag = '%sSingle%s'%(outTag,particleTag)
                    outTag = '%s_E%d'%(outTag,E)
                    outTag = '%sEta%s'%(outTag,etaTag)
                    if phiTag != 'notSet':
                        outTag = '%sPhi%s'%(outTag,phiTag)
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
                    if options.campaign is None or options.campaign == None or options.campaign == 'None':
                        if options.tag is None or options.tag == None or options.tag == 'None':
                            file1.write("'%s_%s_upgrade2026_%s_step2'\n"%(outTag,cmssw,options.geometry))
                        else:
                            file1.write("'%s_%s_upgrade2026_%s_%s_step2'\n"%(outTag,cmssw,options.geometry,options.tag))
                    else:
                        if options.tag is None or options.tag == None or options.tag == 'None':
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
                        file1.write("config.JobType.maxMemoryMB = 10000\n")
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
                    if options.campaign is None or options.campaign == None or options.campaign == 'None':
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
