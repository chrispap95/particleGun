import itertools
import os

from Tools import (
    col,
    enSetup,
    etaSetup,
    fetchData,
    jobSetup,
    phiSetup,
    tagBuilder,
    writeCRABConfig,
)


def ntuples(options):
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
    maxRuntime, memory, nThreads = jobSetup(
        options, maxRuntime=50, memory=2000, nThreads=1
    )

    script = "ntuplesConfig.py"

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
        os.system(f"cp Misc/ntuplesConfig.py myGeneration/{outTag}/")
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
            os.system(f"crab submit -c crabConfig_{outTag}_ntuples.py")

    os.chdir(CWD)
    os.system("rm myGeneration/list.txt")
