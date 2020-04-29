import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

from Tools import mainParserStepN, particleNumbers, col
options = mainParserStepN()
particleTags = particleNumbers()

if __name__ == '__main__':
    # List of energies to shoot
    energies = options.energies
    if energies is None or len(energies) == 0:
        print('%sWarning%s: Energies not specified. Using default values '
        'that might not work in your case.'%(col.magenta,col.endc))
        energies = [1,3,5,10,15,20,25,30]

    # List of etas to shoot particles
    etaTags = options.eta
    if etaTags is None or len(etaTags) == 0:
        print('%sWarning%s: Etas not specified. Using default values '
        'that might not work in your case.'%(col.magenta,col.endc))
        etaTags = ['1p7']
    etas = {}
    for etaTag in etaTags:
        etas[etaTag] = float(etaTag.replace("p","."))

    # List of phi to shoot particles
    phiTags = options.phi
    if phiTags is None or len(phiTags) == 0:
        print('%sWarning%s: Phi not specified. The script is not '
        'going to specify a Phi.'%(col.magenta,col.endc))
        phiTags = ['notSet']
    phis = {}
    for phiTag in phiTags:
        if phiTag != 'notSet':
            phis[phiTag] = float(phiTag.replace("p","."))

    # List of particles to generate in pdg codes
    particles = options.particles
    if particles is None or len(particles) == 0:
        print('%sWarning%s: Particles not specified. Using Gamma as default. '
        'This might not be compatible with your configuration.'%(col.magenta,col.endc))
        particles = [22]

    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    user = os.environ['USER']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

    # Run cmsdriver.py to create workflows
    print('Creating step3 configuration.')
    os.system('cmsDriver.py step3 --conditions auto:phase2_realistic_T19 -n 100 '
    '--era Phase2C9 --procModifier phase2_PixelCPEGeneric --eventcontent FEVTDEBUGHLT '
    '-s RAW2DIGI,L1Reco,RECO,RECOSIM,PAT,VALIDATION:@phase2Validation+@miniAODValidation,DQM:@phase2+@miniAODDQM '
    '--runUnscheduled --no_exec --datatier GEN-SIM-RECO --geometry Extended2026%s '
    '--filein  file:step2.root --fileout file:step3.root'%options.geometry)

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
    os.system("sh createList.sh step2 '%s' '%s' '%s' '%s' '%s'"%(eTag,pTag,options.geometry,etaList,phiList))
    filein = open('myGeneration/list.txt','r')

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
                    os.chdir(cwd)
                    os.system('cp step3_RAW2DIGI_L1Reco_RECO_RECOSIM_PAT_VALIDATION_DQM.py myGeneration/%s/'%outTag)
                    os.chdir('myGeneration/%s'%outTag)

                    # Create CRAB configuration file
                    file1 = open('crabConfig_%s_step3.py'%outTag,'w')
                    file1.write('# Script automatically generated using generator.py\n\n')

                    file1.write('from CRABClient.UserUtilities ')
                    file1.write('import config\n')
                    file1.write('config = config()\n')
                    file1.write("config.General.requestName = ")
                    if options.tag is None or options.tag == None:
                        file1.write("'%s_%s_upgrade2026_%s_step3'\n"%(outTag,cmssw,options.geometry))
                    else:
                        file1.write("'%s_%s_upgrade2026_%s_%s_step3'\n"%(outTag,cmssw,options.geometry,options.tag))
                    file1.write("config.General.workArea = 'crab_projects'\n")
                    file1.write("config.General.transferOutputs = True\n")
                    file1.write("config.General.transferLogs = True\n\n")

                    file1.write("config.JobType.pluginName = 'Analysis'\n")
                    file1.write("config.JobType.maxMemoryMB = 5000\n")
                    file1.write("config.JobType.psetName = ")
                    file1.write("'step3_RAW2DIGI_L1Reco_RECO_RECOSIM_PAT_VALIDATION_DQM.py'\n")
                    file1.write("config.JobType.maxJobRuntimeMin = 50\n\n")

                    file1.write("config.Data.inputDataset = '%s'\n"%((filein.readline())[:-1]))
                    file1.write("config.Data.inputDBS = 'phys03'\n")
                    file1.write("config.Data.splitting = 'FileBased'\n")
                    file1.write("config.Data.unitsPerJob = %d\n"%options.unitsPerJob)
                    file1.write("config.Data.totalUnits = %d\n"%options.njobs)
                    file1.write("config.Data.outLFNDirBase = '/store/user/%s/'\n"%user)
                    file1.write("config.Data.publication = True\n")
                    file1.write("config.Data.outputDatasetTag = ")
                    file1.write("'%s_%s_upgrade2026_%s_step3'\n\n"%(outTag,cmssw,options.geometry))

                    file1.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")
                    file1.write("config.Site.blacklist = ['T2_US_Caltech']\n")
                    file1.close()

                    if !options.no_exec:
                        os.system('crab submit -c crabConfig_%s_step3.py'%outTag)

os.chdir(cwd)
os.system('rm step3_RAW2DIGI_L1Reco_RECO_RECOSIM_PAT_VALIDATION_DQM.py')
