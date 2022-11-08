import math
import os
import sys

from Tools import col, mainParser, makeTag, particleNumbers, tagBuilder

sys.path.append(os.path.abspath(os.path.curdir))

options = mainParser()

if __name__ == "__main__":
    # Getting environment info
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
            col.magenta + "Warning: " + col.endc + "Particles not specified. "
            "Using Gamma as default. This might not be compatible with your configuration."
        )
        particles = [22]

    # List of delta values
    deltas = options.delta
    if deltas is None or len(deltas) == 0:
        deltas = [10.0]

    # Pack the ranges into an array
    ranges = [minEn, maxEn, minEta, maxEta, minPhi, maxPhi]

    iterator = itertools.product(particles, energies, etas, phis, deltas)

    for p, E, eta, phi, delta in iterator:
                        # Append particle, energy, eta and phi tags. Phi tag is skipped if full range is used
                        # and create printout message.
                        outTag = tagBuilder(options, p, E, eta, phi, ranges, delta)
                        print(
                            f"{col.bold}Campaign: {col.magenta}{options.campaign}{col.endc}\t{col.bold}Tag: {col.magenta}{options.tag}{col.endc}"
                        )
                        os.chdir(CWD)
                        os.chdir(f"myGeneration/{outTag}/crab_projects/")

                        listCommand = (
                            f"ls | grep {options.step} | grep {options.geometry}"
                        )
                        if options.campaign is not None:
                            listCommand = f"{listCommand}| grep {options.campaign} "
                        if options.tag is not None:
                            listCommand = f"{listCommand}| grep {options.tag} "
                        if options.delta is not None:
                            listCommand = f"{listCommand}| grep Delta{makeTag(delta)} "
                        if options.overlapping:
                            listCommand = f"{listCommand}| grep Overlapping "
                        if options.pointing is False:
                            listCommand = f"{listCommand}| grep Parallel "
                        listCommand = f"{listCommand}> submissions.txt"
                        os.system(listCommand)

                        fSubmissions = open("submissions.txt")
                        for submission in fSubmissions:
                            os.system("crab kill -d {submission}")
                        os.system("rm submissions.txt")
