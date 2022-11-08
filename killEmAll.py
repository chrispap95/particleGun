import itertools
import math
import os
import sys

from Tools import col, enSetup, etaSetup, mainParser, makeTag, phiSetup, tagBuilder

sys.path.append(os.path.abspath(os.path.curdir))


def killEmAll(options):
    # Getting environment info
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

        listCommand = f"ls | grep {options.step} | grep {options.geometry}"
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
            os.system(f"crab kill -d {submission}")
        os.system("rm submissions.txt")


if __name__ == "__main__":
    options = mainParser()
    killEmAll(options)
