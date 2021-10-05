import os, sys, math
from Tools import particleNumbers, col, makeTag, tagBuilder, setRanges, writeCRABConfig

def step1(options):
    # Getting environment info
    CMSSW = os.environ['CMSSW_VERSION']
    CMSSW_BASE = os.environ['CMSSW_BASE']
    USER = os.environ['USER']
    GEN_DIR = '%s/src/Configuration/GenProduction/python/'%CMSSW_BASE
    CWD = os.getcwd()

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

    # Pack the ranges into an array
    ranges = [minEn, maxEn, minEta, maxEta, minPhi, maxPhi]

    # List of particles to generate in pdg codes
    particleTags = particleNumbers()
    particles = options.particles
    if particles is None or len(particles) == 0:
        print(col.magenta+'Warning: '+col.endc+'Particle not specified. '
        'Using Gamma as default. This might not be compatible with your configuration.')
        particles = [22]

    # List of delta values
    deltas = options.delta
    if deltas is None or len(deltas) == 0:
        deltas = [10.0]

    # Get memory, maxTime and numCores configuration
    maxRuntime = 600
    if options.maxRuntime is not None:
        maxRuntime = options.maxRuntime
    memory = 2000
    if options.memory is not None:
        memory = options.memory
    nThreads = 1
    if options.cpu is not None:
        nThreads = options.cpu

    # Add any process modifiers
    if options.proc is not None:
        proc = options.proc

    for p in particles:
        for E in energies:
            for eta in etas:
                for phi in phis:
                    for delta in deltas:
                        # Append particle, energy, eta and phi tags. Phi tag is skipped
                        # if full range is used and create printout message.
                        outTag = tagBuilder(options, p, E, eta, phi, ranges, delta)
                        ranges = setRanges(E, eta, phi, ranges)

                        # Create working directory
                        os.chdir(CWD)
                        os.system('mkdir -pv myGeneration/%s'%outTag)

                        # Create generator configurations
                        if options.closeBy:
                            zmin = 320;
                            zmax = 321;
                            rmin = zmin*math.tan(2*math.atan(math.exp(-ranges[3])));
                            rmax = zmax*math.tan(2*math.atan(math.exp(-ranges[2])));
                            file0 = open('%s%s_cfi.py'%(GEN_DIR,outTag),'w')
                            file0.write("# Generator fragment automatically generated by submit.py\n\n")
                            file0.write("import FWCore.ParameterSet.Config as cms\n\n")
                            file0.write("generator = cms.EDProducer('CloseByParticleGunProducer',\n")
                            file0.write("\tPGunParameters = cms.PSet(\n")
                            file0.write("\t\tPartID = cms.vint32(%d),\n"%p)
                            file0.write("\t\tEnMax = cms.double(%f),\n"%(ranges[1]))
                            file0.write("\t\tEnMin = cms.double(%f),\n"%(ranges[0]))
                            file0.write("\t\tRMax = cms.double(%f),\n"%(rmax))
                            file0.write("\t\tRMin = cms.double(%f),\n"%(rmin))
                            file0.write("\t\tZMax = cms.double(%f),\n"%(zmax))
                            file0.write("\t\tZMin = cms.double(%f),\n"%(zmin))
                            file0.write("\t\tDelta = cms.double(%f),\n"%(delta))
                            file0.write("\t\tPointing = cms.bool(%s),\n"%(options.pointing))
                            file0.write("\t\tOverlapping = cms.bool(%s),\n"%(options.overlapping))
                            file0.write("\t\tRandomShoot = cms.bool(False),\n")
                            file0.write("\t\tNParticles = cms.int32(%d),\n"%(options.nParticles))
                            file0.write("\t\tMaxEta = cms.double(%f),\n"%(ranges[3]))
                            file0.write("\t\tMinEta = cms.double(%f),\n"%(ranges[2]))
                            file0.write("\t\tMaxPhi = cms.double(%.11f),\n"%(ranges[5]))
                            file0.write("\t\tMinPhi = cms.double(%.11f)\n"%(ranges[4]))
                            file0.write("\t),\n")
                            file0.write("\tVerbosity = cms.untracked.int32(0),\n")
                            file0.write("\tpsethack = cms.string('%s'),\n"%outTag)
                            file0.write("\tAddAntiParticle = cms.bool(False),\n")
                            file0.write("\tfirstRun = cms.untracked.uint32(1),\n")
                            file0.write(")\n")
                            file0.close()
                        else:
                            file0 = open('%s%s_pythia8_cfi.py'%(GEN_DIR,outTag),'w')
                            file0.write("# Generator fragment automatically generated by submit.py\n\n")
                            file0.write("import FWCore.ParameterSet.Config as cms\n\n")
                            file0.write("generator = cms.EDFilter('Pythia8EGun',\n")
                            file0.write("\tPGunParameters = cms.PSet(\n")
                            file0.write("\t\tMaxE = cms.double(%f),\n"%(ranges[1]))
                            file0.write("\t\tMinE = cms.double(%f),\n"%(ranges[0]))
                            file0.write("\t\tParticleID = cms.vint32(%d),\n"%p)
                            file0.write("\t\tAddAntiParticle = cms.bool(False),\n")
                            file0.write("\t\tMaxEta = cms.double(%f),\n"%(ranges[3]))
                            file0.write("\t\tMinEta = cms.double(%f),\n"%(ranges[2]))
                            file0.write("\t\tMaxPhi = cms.double(%f),\n"%(ranges[5]))
                            file0.write("\t\tMinPhi = cms.double(%f)\n"%(ranges[4]))
                            file0.write("\t),\n")
                            file0.write("\tVerbosity = cms.untracked.int32(0), ")
                            file0.write("## set to 1 (or greater)  for printouts\n")
                            file0.write("\tpsethack = cms.string('%s'),\n"%outTag)
                            file0.write("\tfirstRun = cms.untracked.uint32(1),\n")
                            file0.write("\tPythiaParameters = cms.PSet(parameterSets ")
                            file0.write("= cms.vstring())\n\t)\n")
                            file0.close()

                        # Run cmsdriver.py to create workflows
                        os.chdir('%s/myGeneration/%s'%(CWD,outTag))
                        pythiaTag = '_pythia8'
                        if options.closeBy:
                            pythiaTag = ''
                        proc = ''

                        os.system('cmsDriver.py Configuration/GenProduction/python/%s%s_cfi.py '
                            '--mc --conditions auto:%s -n 100 --era %s --eventcontent FEVTDEBUG '
                            '-s GEN,SIM --datatier GEN-SIM --no_exec --beamspot HLLHC --geometry '
                            'Extended2026%s --nThreads %d --fileout file:step1.root %s'%(
                                outTag, pythiaTag, options.conditions, options.era,
                                options.geometry, nThreads, proc
                            )
                        )

                        # Create CRAB configuration file
                        filein = None
                        script = '%s%s_cfi_py_GEN_SIM.py'%(outTag,pythiaTag)
                        writeCRABConfig(options, outTag, nThreads, memory,
                                        maxRuntime, filein, CMSSW, USER, script)

                        if options.no_exec:
                            os.system('crab submit -c crabConfig_%s_step1.py'%outTag)
