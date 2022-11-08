import math
import os

from Tools import col, fetchData, particleNumbers, tagBuilder, writeCRABConfig


def step3(options):
    # Getting environment info
    CMSSW = os.environ["CMSSW_VERSION"]
    USER = os.environ["USER"]
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

    # List of particles to generate in pdg codes
    particleTags = particleNumbers()
    particles = options.particles
    if particles is None or len(particles) == 0:
        print(
            f"{col.magenta}Warning{col.endc}: Particles not specified. Using Gamma as default. "
            "This might not be compatible with your configuration."
        )
        particles = [22]

    # List of delta values
    deltas = options.delta
    if deltas is None or len(deltas) == 0:
        deltas = [10.0]

    # Pack the ranges into an array
    ranges = [minEn, maxEn, minEta, maxEta, minPhi, maxPhi]

    # Get memory, maxTime and numCores configuration
    maxRuntime = 50
    if options.maxRuntime is not None:
        maxRuntime = options.maxRuntime
    memory = 5000
    if options.memory is not None:
        memory = options.memory
    nThreads = 4
    if options.cpu is not None:
        nThreads = options.cpu

    # Pileup configuration
    pileupInput = ""
    pileupConfig = ""
    if options.pileup:
        pileupInput = f"--pileup_input das:{options.pileupInput}"
        pileupConfig = f"--pileup {options.pileupConfig}"
        nThreads = "8"

    if options.cpu is not None:
        nThreads = options.cpu

    # Add any process modifiers
    proc = ""
    if options.proc is not None:
        proc = "--procModifier " + options.proc

    # Run cmsdriver.py to create workflows
    print("Creating step3 configuration.")
    os.system(
        f"cmsDriver.py step3 --conditions auto:{options.conditions} "
        f"-n 100 {pileupInput} {pileupConfig} --era {options.era} "
        f"--eventcontent FEVTDEBUGHLT --no_exec -s RAW2DIGI,L1Reco,RECO,RECOSIM "
        f"--mc --datatier GEN-SIM-RECO --geometry Extended2026{options.geometry} "
        f"--nThreads {nThreads} --filein file:step2.root --fileout file:step3.root {proc}"
    )
    script = "step3_RAW2DIGI_L1Reco_RECO_RECOSIM.py"
    if options.pileup:
        script = "step3_RAW2DIGI_L1Reco_RECO_RECOSIM_PU.py"

    for p in particles:
        for E in energies:
            for eta in etas:
                for phi in phis:
                    for delta in deltas:
                        # Get filenames from previous step
                        filein = fetchData(
                            options,
                            E,
                            p,
                            eta,
                            phi,
                            ranges,
                            delta,
                            CMSSW,
                            USER,
                        )

                        # Append particle, energy, eta and phi tags. Phi tag is skipped
                        # if full range is used and create printout message.
                        outTag = tagBuilder(options, p, E, eta, phi, ranges, delta)

                        os.chdir(CWD)
                        os.system(f"cp {script} myGeneration/{outTag}/")
                        os.chdir(f"myGeneration/{outTag}")

                        # Create CRAB configuration file
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
                            os.system(f"crab submit -c crabConfig_{outTag}_step3.py")

    os.chdir(CWD)
    os.system(f"rm {script}")
