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
        'This might not be compatible with your configuration.')
        particles = [22]

    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

    # Get filenames from previous step
    eTag = ''
    for E in energies:
        eTag = '%s %d'%(eTag,E)
    pTag = ''
    for p in particles:
        pTag = '%s %d'%(pTag,p)
    os.system("sh createList.sh step3 '%s' '%s'"%(eTag,pTag))
    filein = open('myGeneration/list.txt','r')

    for p in particles:
        for E in energies:
            for etaTag in etaTags:
                particleTag = particleTags[p]
                outTag = 'Single%s'%particleTag
                outTag = '%s_E%d'%(outTag,E)
                outTag = '%sEta%s'%(outTag,etaTag)
                os.chdir(cwd)
                os.system('cp run_HGCalTupleMaker_2023.py myGeneration/%s/'%outTag)
                os.chdir('myGeneration/%s'%outTag)

                # Create CRAB configuration file
                file1 = open('crabConfig_%s_ntuples.py'%outTag,'w')
                file1.write('# Script automatically generated using ntuples.py\n\n')
                file1.write('from CRABClient.UserUtilities ')
                file1.write('import config, getUsernameFromSiteDB\n')
                file1.write('config = config()\n')
                file1.write("config.General.requestName = ")
                file1.write("'%s_%s_upgrade2023_%s_ntuples'\n"%(outTag,cmssw,options.geometry))
                file1.write("config.General.workArea = 'crab_projects'\n")
                file1.write("config.General.transferOutputs = True\n")
                file1.write("config.General.transferLogs = True\n\n")
                file1.write("config.JobType.pluginName = 'Analysis'\n")
                file1.write("config.JobType.psetName = ")
                file1.write("'run_HGCalTupleMaker_2023.py'\n\n")
                file1.write("config.Data.inputDataset = '%s'\n"%((filein.readline())[:-1]))
                file1.write("config.Data.inputDBS = 'phys03'\n")
                file1.write("config.Data.splitting = 'FileBased'\n")
                file1.write("config.Data.unitsPerJob = %d\n"%options.unitsPerJob)
                file1.write("config.Data.totalUnits = %d\n"%options.njobs)
                file1.write("config.Data.outLFNDirBase = '/store/user/%s/' ")
                file1.write("% (getUsernameFromSiteDB())\n")
                file1.write("config.Data.publication = False\n")
                file1.write("config.Data.outputDatasetTag = ")
                file1.write("'%s_%s_upgrade2023_%s_ntuples'\n\n"%(outTag,cmssw,options.geometry))
                file1.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")
                file1.close()

                os.system('crab submit -c crabConfig_%s_ntuples.py'%outTag)

os.chdir(cwd)
os.system('rm myGeneration/list.txt')
