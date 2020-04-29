import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

from Tools import mainParserStep1, particleNumbers, col
options = mainParserStep1()
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
        'Using Gamma as default. This might not be compatible with your configuration.')
        particles = [22]

    # Getting environment info
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    user = os.environ['USER']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    cwd = os.getcwd()

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
                    os.system('mkdir -p myGeneration/%s'%outTag)
                    if phiTag != 'notSet':
                        print('Creating configuration for %s at E=%d Eta=%s Phi=%s.'%(particleTag,E,etaTag,phiTag))
                    else:
                        print('Creating configuration for %s at E=%d Eta=%s.'%(particleTag,E,etaTag))

                    # Create generator configurations
                    file0 = open('%s%s_pythia8_cfi.py'%(genDir,outTag),'w')
                    file0.write("# Generator fragment automatically generated by step1.py script\n\n")
                    file0.write("import FWCore.ParameterSet.Config as cms\n\n")
                    file0.write("generator = cms.EDFilter('Pythia8EGun',\n")
                    file0.write("\tPGunParameters = cms.PSet(\n")
                    file0.write("\t\tMaxE = cms.double(%f),\n"%(E+0.01))
                    file0.write("\t\tMinE = cms.double(%f),\n"%(E-0.01))
                    file0.write("\t\tParticleID = cms.vint32(%d),\n"%p)
                    file0.write("\t\tAddAntiParticle = cms.bool(True),\n")
                    file0.write("\t\tMaxEta = cms.double(%f),\n"%etas[etaTag])
                    file0.write("\t\tMinEta = cms.double(%f),\n"%etas[etaTag])
                    if phiTag != 'notSet':
                        file0.write("\t\tMaxPhi = cms.double(%f),\n"%phis[phiTag])
                        file0.write("\t\tMinPhi = cms.double(%f)\n"%phis[phiTag])
                    else:
                        file0.write("\t\tMaxPhi = cms.double(3.14159265359),\n")
                        file0.write("\t\tMinPhi = cms.double(-3.14159265359) ## in radians\n")
                    file0.write("\t),\n")
                    file0.write("\tVerbosity = cms.untracked.int32(0), ")
                    file0.write("## set to 1 (or greater)  for printouts\n")
                    file0.write("\tpsethack = cms.string('%s'),\n"%outTag)
                    file0.write("\tfirstRun = cms.untracked.uint32(1),\n")
                    file0.write("\tPythiaParameters = cms.PSet(parameterSets ")
                    file0.write("= cms.vstring())\n\t)\n")
                    file0.close()

                    # Run cmsdriver.py to create workflows
                    os.chdir('%s/myGeneration/%s'%(cwd,outTag))
                    os.system('cmsDriver.py Configuration/GenProduction/python/%s_pythia8_cfi.py '
                    '--conditions auto:phase2_realistic_T19 --procModifier phase2_PixelCPEGeneric '
                    '-n 100 --era Phase2C9 --eventcontent FEVTDEBUG --relval 9000,50 -s GEN,SIM '
                    '--datatier GEN-SIM --no_exec --beamspot HLLHC --geometry Extended2026%s '
                    '--fileout file:step1.root'%(outTag,options.geometry))

                    # Create CRAB configuration file
                    file1 = open('crabConfig_%s_step1.py'%outTag,'w')
                    file1.write('# Script automatically generated by step1.py\n\n')

                    file1.write('from CRABClient.UserUtilities ')
                    file1.write('import config\n')
                    file1.write('config = config()\n')
                    file1.write("config.General.requestName = ")
                    if options.tag is None or options.tag == None:
                        file1.write("'%s_%s_upgrade2026_%s_step1'\n"%(outTag,cmssw,options.geometry))
                    else:
                        file1.write("'%s_%s_upgrade2026_%s_%s_step1'\n"%(outTag,cmssw,options.geometry,options.tag))
                    file1.write("config.General.workArea = 'crab_projects'\n")
                    file1.write("config.General.transferOutputs = True\n")
                    file1.write("config.General.transferLogs = False\n\n")

                    file1.write("config.JobType.pluginName = 'PrivateMC'\n")
                    file1.write("config.JobType.psetName = ")
                    file1.write("'%s_pythia8_cfi_py_GEN_SIM.py'\n"%outTag)
                    file1.write("config.JobType.maxJobRuntimeMin = 600\n\n")

                    file1.write("config.Data.outputPrimaryDataset = '%s'\n"%outTag)
                    file1.write("config.Data.splitting = 'EventBased'\n")
                    file1.write("config.Data.unitsPerJob = %d\n"%options.unitsPerJob)
                    file1.write("NJOBS = %d  # This is not a configuration parameter,"%options.njobs)
                    file1.write(" but an auxiliary variable that we use in the next line.\n")
                    file1.write("config.Data.totalUnits = config.Data.unitsPerJob * NJOBS\n")
                    file1.write("config.Data.outLFNDirBase = '/store/user/%s/'\n"%user)
                    file1.write("config.Data.publication = True\n")
                    file1.write("config.Data.outputDatasetTag = ")
                    file1.write("'%s_%s_upgrade2026_%s_step1'\n\n"%(outTag,cmssw,options.geometry))

                    file1.write("config.Site.blacklist = ['T2_US_Caltech']\n")
                    file1.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")
                    file1.close()

                    if !options.no_exec:
                        os.system('crab submit -c crabConfig_%s_step1.py'%outTag)
