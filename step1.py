import os, sys, math

sys.path.append(os.path.abspath(os.path.curdir))

from Tools import mainParserStep1, particleNumbers, col
options = mainParserStep1()
particleTags = particleNumbers()

if __name__ == '__main__':
    # List or range of energies to shoot particles
    minEn, maxEn = 0, 650
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
    minEta, maxEta = 1.5, 3.0
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
    etas = {}
    for etaTag in etaTags:
        if etaTag != 'notSet':
            etas[etaTag] = float(etaTag.replace("p","."))

    # List or range of phi to shoot particles
    minPhi, maxPhi = -math.pi, math.pi
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
    phis = {}
    for phiTag in phiTags:
        if phiTag != 'notSet':
            phis[phiTag] = float(phiTag.replace("p","."))

    # List of particles to generate in pdg codes
    particles = options.particles
    if particles is None or len(particles) == 0:
        print(col.magenta+'Warning: '+col.endc+'Particle not specified. '
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
                    if E is 'notSet':
                        outTag = '%s_E%sto%s'%(outTag,minEnTag,maxEnTag)
                        printOut = '%sE in (%s,%s) GeV, '%(printOut,minEnTag,maxEnTag)
                    else:
                        outTag = '%s_E%d'%(outTag,E)
                        printOut = '%sE=%d GeV, '%(printOut,E)
                        minEn, maxEn = E-0.01, E+0.01
                    if etaTag is 'notSet':
                        outTag = '%sEta%sto%s'%(outTag,minEtaTag,maxEtaTag)
                        printOut = '%seta in (%s,%s), '%(printOut,minEtaTag,maxEtaTag)
                    else:
                        outTag = '%sEta%s'%(outTag,etaTag)
                        printOut = '%seta=%s, '%(printOut,etaTag)
                        minEta, maxEta = etas[etaTag]-0.01, etas[etaTag]+0.01
                    if phiTag is 'notSet':
                        if options.minPhi is not None or options.maxPhi is not None:
                            outTag = '%sPhi%sto%s'%(outTag,minPhiTag,maxPhiTag)
                        printOut = '%sand phi in (%s,%s)%s'%(printOut,minPhiTag,maxPhiTag,col.endc)
                    else:
                        outTag = '%sPhi%s'%(outTag,phiTag)
                        printOut = '%sand phi=%s%s'%(printOut,phiTag,col.endc)
                        minPhi, maxPhi = phis[phiTag]-0.01, phis[phiTag]+0.01
                    print(printOut)

                    # Create working directory
                    os.chdir(cwd)
                    os.system('mkdir -pv myGeneration/%s'%outTag)

                    # Create generator configurations
                    if options.closeBy:
                        zmin = 320;
                        zmax = 321;
                        rmin = zmin*math.tan(2*math.atan(math.exp(-maxEta)));
                        rmax = zmax*math.tan(2*math.atan(math.exp(-minEta)));
                        file0 = open('%s%s_cfi.py'%(genDir,outTag),'w')
                        file0.write("# Generator fragment automatically generated by step1.py script\n\n")
                        file0.write("import FWCore.ParameterSet.Config as cms\n\n")
                        file0.write("generator = cms.EDProducer('CloseByParticleGunProducer',\n")
                        file0.write("\tPGunParameters = cms.PSet(\n")
                        file0.write("\t\tPartID = cms.vint32(%d),\n"%p)
                        file0.write("\t\tEnMax = cms.double(%f),\n"%(maxEn))
                        file0.write("\t\tEnMin = cms.double(%f),\n"%(minEn))
                        file0.write("\t\tRMax = cms.double(%f),\n"%(rmax))
                        file0.write("\t\tRMin = cms.double(%f),\n"%(rmin))
                        file0.write("\t\tZMax = cms.double(%f),\n"%(zmax))
                        file0.write("\t\tZMin = cms.double(%f),\n"%(zmin))
                        file0.write("\t\tDelta = cms.double(10),\n")
                        file0.write("\t\tPointing = cms.bool(True),\n")
                        file0.write("\t\tOverlapping = cms.bool(False),\n")
                        file0.write("\t\tRandomShoot = cms.bool(False),\n")
                        file0.write("\t\tNParticles = cms.int32(1),\n")
                        file0.write("\t\tMaxEta = cms.double(%f),\n"%(maxEta))
                        file0.write("\t\tMinEta = cms.double(%f),\n"%(minEta))
                        file0.write("\t\tMaxPhi = cms.double(%.11f),\n"%(maxPhi))
                        file0.write("\t\tMinPhi = cms.double(%.11f)\n"%(minPhi))
                        file0.write("\t),\n")
                        file0.write("\tVerbosity = cms.untracked.int32(0),\n")
                        file0.write("\tpsethack = cms.string('%s'),\n"%outTag)
                        file0.write("\tAddAntiParticle = cms.bool(False),\n")
                        file0.write("\tfirstRun = cms.untracked.uint32(1),\n")
                        file0.write(")\n")
                        file0.close()
                    else:
                        file0 = open('%s%s_pythia8_cfi.py'%(genDir,outTag),'w')
                        file0.write("# Generator fragment automatically generated by step1.py script\n\n")
                        file0.write("import FWCore.ParameterSet.Config as cms\n\n")
                        file0.write("generator = cms.EDFilter('Pythia8EGun',\n")
                        file0.write("\tPGunParameters = cms.PSet(\n")
                        file0.write("\t\tMaxE = cms.double(%f),\n"%(maxEn))
                        file0.write("\t\tMinE = cms.double(%f),\n"%(minEn))
                        file0.write("\t\tParticleID = cms.vint32(%d),\n"%p)
                        file0.write("\t\tAddAntiParticle = cms.bool(False),\n")
                        file0.write("\t\tMaxEta = cms.double(%f),\n"%(maxEta))
                        file0.write("\t\tMinEta = cms.double(%f),\n"%(minEta))
                        file0.write("\t\tMaxPhi = cms.double(%f),\n"%(maxPhi))
                        file0.write("\t\tMinPhi = cms.double(%f)\n"%(minPhi))
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
                    pythiaTag = '_pythia8'
                    if options.closeBy:
                        pythiaTag = ''
                    os.system('cmsDriver.py Configuration/GenProduction/python/%s%s_cfi.py --mc '
                    '--conditions auto:%s -n 100 --era %s --eventcontent FEVTDEBUG -s GEN,SIM '
                    '--datatier GEN-SIM --no_exec --beamspot HLLHC --geometry Extended2026%s '
                    '--fileout file:step1.root'%(outTag,pythiaTag,options.conditions,options.era,options.geometry))

                    # Create CRAB configuration file
                    file1 = open('crabConfig_%s_step1.py'%outTag,'w')
                    file1.write('# Script automatically generated by step1.py\n\n')

                    file1.write('from CRABClient.UserUtilities ')
                    file1.write('import config\n')
                    file1.write('config = config()\n')
                    file1.write("config.General.requestName = ")
                    if options.campaign is None:
                        if options.tag is None:
                            file1.write("'%s_%s_upgrade2026_%s_step1'\n"%(outTag,cmssw,options.geometry))
                        else:
                            file1.write("'%s_%s_upgrade2026_%s_%s_step1'\n"%(outTag,cmssw,options.geometry,options.tag))
                    else:
                        if options.tag is None:
                            file1.write("'%s_%s_upgrade2026_%s_%s_step1'\n"%(outTag,cmssw,options.geometry,options.campaign))
                        else:
                            file1.write("'%s_%s_upgrade2026_%s_%s_%s_step1'\n"%(outTag,cmssw,options.geometry,options.campaign,options.tag))
                    file1.write("config.General.workArea = 'crab_projects'\n")
                    file1.write("config.General.transferOutputs = True\n")
                    file1.write("config.General.transferLogs = False\n\n")

                    file1.write("config.JobType.pluginName = 'PrivateMC'\n")
                    file1.write("config.JobType.psetName = ")
                    file1.write("'%s%s_cfi_py_GEN_SIM.py'\n"%(outTag,pythiaTag))
                    if options.memory is not None:
                        file1.write("config.JobType.maxMemoryMB = %s\n"%options.memory)
                    if options.cpu is not None:
                        file1.write("config.JobType.numCores = %s\n"%options.cpu)
                    file1.write("config.JobType.maxJobRuntimeMin = 600\n\n")

                    file1.write("config.Data.outputPrimaryDataset = '%s'\n"%outTag)
                    file1.write("config.Data.splitting = 'EventBased'\n")
                    file1.write("config.Data.unitsPerJob = %d\n"%options.unitsPerJob)
                    file1.write("NJOBS = %d  # This is not a configuration parameter,"%options.njobs)
                    file1.write(" but an auxiliary variable that we use in the next line.\n")
                    file1.write("config.Data.totalUnits = config.Data.unitsPerJob * NJOBS\n")
                    file1.write("config.Data.outLFNDirBase = '%s%s/'\n"%(options.dest,user))
                    file1.write("config.Data.publication = True\n")
                    file1.write("config.Data.outputDatasetTag = ")
                    if options.campaign is None:
                        file1.write("'%s_%s_upgrade2026_%s_step1'\n\n"%(outTag,cmssw,options.geometry))
                    else:
                        file1.write("'%s_%s_upgrade2026_%s_%s_step1'\n\n"%(outTag,cmssw,options.geometry,options.campaign))

                    file1.write("config.Site.blacklist = ['T2_US_Caltech']\n")
                    file1.write("config.Site.storageSite = '%s'\n"%options.site)
                    file1.close()

                    if options.no_exec:
                        os.system('crab submit -c crabConfig_%s_step1.py'%outTag)
