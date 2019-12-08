import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

from Tools import mainParserStepN, particleNumbers
options = mainParserStepN()
particleTags = particleNumbers()

if __name__ == '__main__':
    # List of energies to shoot
    energies = options.energies
    if energies is None or len(energies) == 0:
        print('Energies not specified. '
        'Using default values that might not work in your case.')
        energies = [1,3,5,10,15,20,25,30]

    # List of etas to shoot particles
    etaTags = ['1p7']
    etas = {}
    etas['1p7'] = 1.7

    # List of particles to generate in pdg codes
    particles = options.particles
    if particles is None or len(particles) == 0:
        print('Particles not specified. Using Gamma as default. '
        'This might not be compatible with your configuration.\n')
        particles = [22]

    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

    # Run cmsdriver.py to create workflows
    print('Creating step2 configuration.')
    os.system('cmsDriver.py step2 --conditions auto:phase2_realistic '
    '-s DIGI:pdigi_valid,L1,L1TrackTrigger,DIGI2RAW,HLT:@fake2 '
    '--datatier GEN-SIM-DIGI-RAW -n 100 --geometry Extended2023%s '
    '--era Phase2C8_timing_layer_bar --eventcontent FEVTDEBUGHLT '
    '--no_exec --filein file:step1.root --fileout file:step2.root'%options.geometry)

    # Get filenames from previous step
    eTag = ''
    for E in energies:
        eTag = '%s %d'%(eTag,E)
    pTag = ''
    for p in particles:
        pTag = '%s %d'%(pTag,p)
    os.system("sh createList.sh step1 '%s' '%s'"%(eTag,pTag))
    filein = open('myGeneration/list.txt','r')

    for p in particles:
        for E in energies:
            for etaTag in etaTags:
                particleTag = particleTags[p]
                outTag = 'Single%s'%particleTag
                outTag = '%s_E%d'%(outTag,E)
                outTag = '%sEta%s'%(outTag,etaTag)
                os.chdir(cwd)
                os.system('cp step2_DIGI_L1_L1TrackTrigger_DIGI2RAW_HLT.py myGeneration/%s/'%outTag)
                os.chdir('myGeneration/%s'%outTag)

                # Create CRAB configuration file
                file1 = open('crabConfig_%s_step2.py'%outTag,'w')
                file1.write('# Script automatically generated by step2.py\n\n')

                file1.write('from CRABClient.UserUtilities ')
                file1.write('import config, getUsernameFromSiteDB\n')
                file1.write('config = config()\n')
                file1.write("config.General.requestName = ")
                if options.tag is None or options.tag == None:
                    file1.write("'%s_%s_upgrade2023_%s_step2'\n"%(outTag,cmssw,options.geometry))
                else:
                    file1.write("'%s_%s_upgrade2023_%s_%s_step2'\n"%(outTag,cmssw,options.geometry,options.tag))
                file1.write("config.General.workArea = 'crab_projects'\n")
                file1.write("config.General.transferOutputs = True\n")
                file1.write("config.General.transferLogs = True\n\n")

                file1.write("config.JobType.pluginName = 'Analysis'\n")
                file1.write("config.JobType.psetName = ")
                file1.write("'step2_DIGI_L1_L1TrackTrigger_DIGI2RAW_HLT.py'\n")
                file1.write("config.JobType.maxJobRuntimeMin = 600\n\n")

                file1.write("config.Data.inputDataset = '%s'\n"%((filein.readline())[:-1]))
                file1.write("config.Data.inputDBS = 'phys03'\n")
                file1.write("config.Data.splitting = 'FileBased'\n")
                file1.write("config.Data.unitsPerJob = %d\n"%options.unitsPerJob)
                file1.write("config.Data.totalUnits = %d\n"%options.njobs)
                file1.write("config.Data.outLFNDirBase = '/store/user/%s/' ")
                file1.write("% (getUsernameFromSiteDB())\n")
                file1.write("config.Data.publication = True\n")
                file1.write("config.Data.outputDatasetTag = ")
                file1.write("'%s_%s_upgrade2023_%s_step2'\n\n"%(outTag,cmssw,options.geometry))

                file1.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")
                file1.write("config.Site.blacklist = ['T2_US_CALTECH']\n")
                file1.close()

                os.system('crab submit -c crabConfig_%s_step2.py'%outTag)

os.chdir(cwd)
os.system('rm step2_DIGI_L1_L1TrackTrigger_DIGI2RAW_HLT.py')
