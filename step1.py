import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

if __name__ == '__main__':
    energies = [1,3,5,10,15,20,25,30] # List of energies of generated particles
    etas = [1.7]                      # List of etas to shoot particles
    particles = [130]                 # List of particles to generate in pdg codes
    geometry = 'D41'                  # Geometry tag. Use >=D41
    cmssw = os.environ('CMSSW_VERSION')
    genDir = '$CMSSW_BASE/src/Configuration/GenProduction/python/'

    for p in particles:
        outTag='SingleK0L'
        for E in energies:
            outTag='%s_%d'%(outTag,E)
            for eta in etas:
                outTag='%s%f'%eta
                os.system('mkdir -p %s'%outTag)
                os.system('cd %s'%outTag)
                print('Creating configuration for K0L at E=%d Eta=%f.'%(E,eta))

                # Create generator configurations
                file0 = open('%s%s_pythia8_cfi.py'%(genDir,outTag))
                file0.write("import FWCore.ParameterSet.Config as cms\n\n")
                file0.write("generator = cms.EDFilter('Pythia8EGun',\n")
                file0.write("\t\t\tPGunParameters = cms.PSet(\n")
                file0.write("\tMaxE = cms.double(%f),\n"%(E+0.01))
                file0.write("\tMinE = cms.double(%f),\n"%(E-0.01))
                file0.write("\tParticleID = cms.vint32(%d),\n"%p)
                file0.write("\tAddAntiParticle = cms.bool(True),\n")
                file0.write("\tMaxEta = cms.double(%f),\n"%eta)
                file0.write("\tMaxPhi = cms.double(3.14159265359),\n")
                file0.write("\tMinEta = cms.double(%f),\n"%eta)
                file0.write("\tMinPhi = cms.double(-3.14159265359) ## in radians\n")
                file0.write("\t),\n")
                file0.write("\t\t\tVerbosity = cms.untracked.int32(0), ")
                file0.write("## set to 1 (or greater)  for printouts\n")
                file0.write("\t\t\tpsethack = cms.string('%s'),\n"%outTag)
                file0.write("\t\t\tfirstRun = cms.untracked.uint32(1),\n")
                file0.write("\t\t\tPythiaParameters = cms.PSet(parameterSets ")
                file0.write("= cms.vstring())\n\t\t\t)\n")
                file0.close()

                # Run cmsdriver.py to create workflows
                os.system('cmsDriver.py Configuration/GenProduction/python/%s_pythia8_cfi.py \
                --conditions auto:phase2_realistic -n 100 --era Phase2C8_timing_layer_bar \
                --eventcontent FEVTDEBUG --relval 9000,50 -s GEN,SIM --datatier GEN-SIM \
                --beamspot HLLHC --geometry Extended2023D41 --fileout file:step1.root')%outTag

                # Create CRAB configuration file
                file1 = open('crabConfig_%s.py'%outTag,'w')
                file1.write('# Script automatically generated using generator.py\n\n')
                file1.write('from CRABClient.UserUtilities ')
                file1.write('import config, getUsernameFromSiteDB\n')
                file1.write('config = config()\n')
                file1.write("config.General.requestName = ")
                file1.write("'%s_%s_upgrade2023_%s_step1'\n"%(outTag,cmssw,geometr))
                file1.write("config.General.workArea = 'crab_projects'\n")
                file1.write("config.General.transferOutputs = True\n")
                file1.write("config.General.transferLogs = False\n\n")
                file1.write("config.JobType.pluginName = 'PrivateMC'\n")
                file1.write("config.JobType.psetName = ")
                file1.write("'%s_pythia8_cfi_py_GEN_SIM.py'\n\n"%outTag)
                file1.write("config.Data.outputPrimaryDataset = '%s'\n"%outTag)
                file1.write("config.Data.splitting = 'EventBased'\n")
                file1.write("config.Data.unitsPerJob = %d\n"%unitsPerJob)
                file1.write("NJOBS = %d  # This is not a configuration parameter,"%njobs)
                file1.write(" but an auxiliary variable that we use in the next line.\n")
                file1.write("config.Data.totalUnits = config.Data.unitsPerJob * NJOBS\n")
                file1.write("config.Data.outLFNDirBase = '/store/user/%s/' ")
                file1.write("% (getUsernameFromSiteDB())\n")
                file1.write("config.Data.publication = True\n")
                file1.write("config.Data.outputDatasetTag = ")
                file1.write("'%s_%s_upgrade2023_%s_step1'\n\n"%(outTag,cmssw,geometry))
                file1.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")
                file1.close()
