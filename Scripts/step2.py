import itertools
import math
import os

from Tools import (
    col,
    enSetup,
    etaSetup,
    fetchData,
    phiSetup,
    tagBuilder,
    writeCRABConfig,
)


def step2(options):
    # Getting environment info
    CMSSW = os.environ["CMSSW_VERSION"]
    USER = os.environ["USER"]
    CWD = os.getcwd()

    # List or range of energies to shoot particles
    energies, minEn, maxEn = enSetup(options)

    # List or range of etas to shoot particles
    etas, minEta, maxEta = etaSetup(options)

    # List or range of phi to shoot particles
    phis, minPhi, maxPhi = phiSetup(options)

    # List of particles to generate in pdg codes
    particles = options.particles
    if particles is None or len(particles) == 0:
        print(
            col.magenta + "Warning: " + col.endc + "Particles not specified. "
            "Using Gamma as default. This might not be compatible with your configuration.\n"
        )
        particles = [22]

    # List of delta values
    deltas = options.delta
    if deltas is None or len(deltas) == 0:
        deltas = [10.0]

    # Pack the ranges into an array
    ranges = [minEn, maxEn, minEta, maxEta, minPhi, maxPhi]

    # Get memory, maxTime and numCores configuration
    maxRuntime = 60
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

    # Add any process modifiers
    proc = ""
    if options.proc is not None:
        proc = "--procModifier " + options.proc

    # Run cmsdriver.py to create workflows
    print("Creating step2 configuration.")
    os.system(
        f"cmsDriver.py step2 --mc --datatier GEN-SIM-DIGI-RAW -n 100 "
        f"-s DIGI:pdigi_valid,L1TrackTrigger,L1,DIGI2RAW,HLT:@fake2 --nThreads {nThreads} --geometry "
        f"Extended2026{options.geometry} {pileupInput} {pileupConfig} --era {options.era} --eventcontent FEVTDEBUGHLT "
        f"--no_exec --conditions auto:{options.conditions} --filein file:step1.root --fileout "
        f"file:step2.root {proc}"
    )
    script = "step2_DIGI_L1TrackTrigger_L1_DIGI2RAW_HLT.py"
    if options.pileup:
        script = "step2_DIGI_L1TrackTrigger_L1_DIGI2RAW_HLT_PU.py"

    iterator = itertools.product(particles, energies, etas, phis, deltas)

    for p, E, eta, phi, delta in iterator:
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
            os.system(f"crab submit -c crabConfig_{outTag}_step2.py")

    os.chdir(CWD)
    os.system(f"rm {script}")
