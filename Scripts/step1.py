import math
import os

from Tools import (
    col,
    compareCMSSWversions,
    particleNumbers,
    setRanges,
    tagBuilder,
    writeCRABConfig,
)


def step1(options):
    # Getting environment info
    CMSSW = os.environ["CMSSW_VERSION"]
    CMSSW_BASE = os.environ["CMSSW_BASE"]
    USER = os.environ["USER"]
    GEN_DIR = f"{CMSSW_BASE}/src/Configuration/GenProduction/python/"
    CWD = os.getcwd()

    # List or range of energies to shoot particles
    minEn, maxEn = 0, 650
    if options.maxEn is not None:
        maxEn = options.maxEn
    if options.minEn is not None:
        minEn = options.minEn
    energies = options.energies
    if energies is None or len(energies) == 0:
        energies = ["notSet"]

    # List or range of etas to shoot particles
    minEta, maxEta = 1.5, 3.0
    if options.maxEta is not None:
        maxEta = options.maxEta
    if options.minEta is not None:
        minEta = options.minEta
    etas = options.eta
    if etas is None or len(etas) == 0:
        etas = ["notSet"]

    # List or range of phi to shoot particles
    minPhi, maxPhi = -math.pi, math.pi
    if options.maxPhi is not None:
        maxPhi = options.maxPhi
    if options.minPhi is not None:
        minPhi = options.minPhi
    phis = options.phi
    if phis is None or len(phis) == 0:
        phis = ["notSet"]

    # Pack the ranges into an array
    ranges = [minEn, maxEn, minEta, maxEta, minPhi, maxPhi]

    # List of particles to generate in pdg codes
    particleTags = particleNumbers()
    particles = options.particles
    if particles is None or len(particles) == 0:
        print(
            col.magenta + "Warning: " + col.endc + "Particle not specified. "
            "Using Gamma as default. This might not be compatible with your configuration."
        )
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

    # Set beamspot
    beamspot = options.beamspot
    if beamspot is None:
        if compareCMSSWversions(CMSSW, "CMSSW_12_1_0_pre2") > -1 and options.closeBy:
            # Ensures no GEN-to-SIM vertex smearing for CloseByParticleGun workflows
            beamspot = "HGCALCloseBy"
        else:
            # Default HLLHC beamspot
            beamspot = "HLLHC"

    # Add any process modifiers
    if options.proc is not None:
        proc = "--procModifier " + options.proc

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
                        os.system(f"mkdir -pv myGeneration/{outTag}")

                        # Create generator configurations
                        if options.closeBy:
                            # Shoot particles in front of the HGCAL (321 cm)
                            ZMIN = 320
                            ZMAX = 321
                            rmin = ZMIN * math.tan(2 * math.atan(math.exp(-ranges[3])))
                            rmax = ZMAX * math.tan(2 * math.atan(math.exp(-ranges[2])))
                            file0 = open(f"{GEN_DIR}{outTag}_cfi.py", "w")
                            file0.write(
                                "# Generator fragment automatically generated by submit.py\n\n"
                            )
                            file0.write("import FWCore.ParameterSet.Config as cms\n\n")
                            file0.write(
                                "generator = cms.EDProducer('CloseByParticleGunProducer',\n"
                            )
                            file0.write("\tPGunParameters = cms.PSet(\n")
                            file0.write(f"\t\tPartID = cms.vint32({p}),\n")
                            if compareCMSSWversions(CMSSW, "CMSSW_12_3_0_pre5"):
                                file0.write("\t\tControlledByEta = cms.bool(False),\n")
                            if compareCMSSWversions(CMSSW, "CMSSW_12_3_0_pre2"):
                                file0.write("\t\tMaxEnSpread = cms.bool(False),\n")
                            file0.write(f"\t\tEnMax = cms.double({ranges[1]}),\n")
                            file0.write(f"\t\tEnMin = cms.double({ranges[0]}),\n")
                            file0.write(f"\t\tRMax = cms.double({rmax}),\n")
                            file0.write(f"\t\tRMin = cms.double({rmin}),\n")
                            file0.write(f"\t\tZMax = cms.double({ZMAX}),\n")
                            file0.write(f"\t\tZMin = cms.double({ZMIN}),\n")
                            file0.write(f"\t\tDelta = cms.double({delta}),\n")
                            file0.write(
                                f"\t\tPointing = cms.bool({options.pointing}),\n"
                            )
                            file0.write(
                                f"\t\tOverlapping = cms.bool({options.overlapping}),\n"
                            )
                            file0.write("\t\tRandomShoot = cms.bool(False),\n")
                            file0.write(
                                f"\t\tNParticles = cms.int32(options.nParticles),\n"
                            )
                            file0.write(f"\t\tMaxEta = cms.double({ranges[3]}),\n")
                            file0.write(f"\t\tMinEta = cms.double({ranges[2]}),\n")
                            file0.write(
                                f"\t\tMaxPhi = cms.double({ranges[5]}),\n"
                            )
                            file0.write(
                                f"\t\tMinPhi = cms.double({ranges[4]})\n"
                            )
                            file0.write("\t),\n")
                            file0.write("\tVerbosity = cms.untracked.int32(0),\n")
                            file0.write(f"\tpsethack = cms.string('{outTag}'),\n")
                            file0.write("\tAddAntiParticle = cms.bool(False),\n")
                            file0.write("\tfirstRun = cms.untracked.uint32(1),\n")
                            file0.write(")\n")
                            file0.close()
                        else:
                            file0 = open(f"{GEN_DIR}{outTag}_pythia8_cfi.py", "w")
                            file0.write(
                                "# Generator fragment automatically generated by submit.py\n\n"
                            )
                            file0.write("import FWCore.ParameterSet.Config as cms\n\n")
                            file0.write("generator = cms.EDFilter('Pythia8EGun',\n")
                            file0.write("\tPGunParameters = cms.PSet(\n")
                            file0.write(f"\t\tMaxE = cms.double({ranges[1]}),\n")
                            file0.write(f"\t\tMinE = cms.double({ranges[0]}),\n")
                            file0.write(f"\t\tParticleID = cms.vint32({p}),\n")
                            file0.write("\t\tAddAntiParticle = cms.bool(False),\n")
                            file0.write(f"\t\tMaxEta = cms.double({ranges[3]}),\n")
                            file0.write(f"\t\tMinEta = cms.double({ranges[2]}),\n")
                            file0.write(f"\t\tMaxPhi = cms.double({ranges[5]}),\n")
                            file0.write(f"\t\tMinPhi = cms.double({ranges[4]})\n")
                            file0.write("\t),\n")
                            file0.write("\tVerbosity = cms.untracked.int32(0), ")
                            file0.write("## set to 1 (or greater)  for printouts\n")
                            file0.write(f"\tpsethack = cms.string('{outTag}'),\n")
                            file0.write("\tfirstRun = cms.untracked.uint32(1),\n")
                            file0.write("\tPythiaParameters = cms.PSet(parameterSets ")
                            file0.write("= cms.vstring())\n\t)\n")
                            file0.close()

                        # Run cmsdriver.py to create workflows
                        os.chdir(f"{CWD}/myGeneration/{outTag}")
                        pythiaTag = "_pythia8"
                        if options.closeBy:
                            pythiaTag = ""
                        proc = ""

                        os.system(
                            f"cmsDriver.py Configuration/GenProduction/python/{outTag}{pythiaTag}_cfi.py "
                            f"--mc --conditions auto:{options.conditions} -n 100 --era {options.era} --eventcontent FEVTDEBUG "
                            f"-s GEN,SIM --datatier GEN-SIM --no_exec --beamspot {beamspot} --geometry "
                            f"Extended2026{options.geometry} --nThreads {nThreads} --fileout file:step1.root {proc}"
                        )

                        # Create CRAB configuration file
                        filein = None
                        script = f"{outTag}{pythiaTag}_cfi_py_GEN_SIM.py"
                        writeCRABConfig(
                            options,
                            outTag,
                            nThreads,
                            memory,
                            maxRuntime,
                            filein,
                            CMSSW,
                            USER,
                            script,
                        )

                        if options.no_exec:
                            os.system(f"crab submit -c crabConfig_{outTag}_step1.py")
