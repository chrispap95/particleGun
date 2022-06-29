#
#  Author: Christos Papageorgakis
#
# Contains option parsing definitions
# and other necessary tools.
#

import argparse
import os
import re
import subprocess


def mainParser():
    parser = argparse.ArgumentParser(
        description="Submit and manage multiple particle gun jobs with CRAB3.",
        usage="%(prog)s [options]",
    )
    parser.add_argument(
        "-s",
        "--step",
        choices=["step1", "step2", "step3", "ntuples"],
        required=True,
        help="Step to be used.",
    )
    parser.add_argument(
        "-g",
        "--geometry",
        default="D76",
        help="Detector geometry for tagging. (Default is D76)",
    )
    parser.add_argument(
        "-n",
        "--njobs",
        type=int,
        default=10,
        help="Number of jobs to run. (Default is 10)",
    )
    parser.add_argument(
        "-u",
        "--unitsPerJob",
        type=int,
        default=10,
        help="Events per job for step1 and files processed per "
        "job for all other steps. (Default is 10)",
    )
    parser.add_argument(
        "-E", "--energies", type=float, nargs="*", help="List of energies to shoot."
    )
    parser.add_argument(
        "-e", "--eta", type=float, nargs="*", help="List of eta to shoot."
    )
    parser.add_argument(
        "-P", "--phi", type=float, nargs="*", help="List of phi to shoot."
    )
    parser.add_argument(
        "-p", "--particles", type=int, nargs="*", help="List of particles to shoot."
    )
    parser.add_argument(
        "-t", "--tag", help="Unique tag to discern between different submissions."
    )
    parser.add_argument("-i", "--inputTag", help="Tag of input dataset.")
    parser.add_argument("-c", "--campaign", help="Adds a tag to outputDatasetTag.")
    parser.add_argument(
        "--inputCampaign",
        help="Searches for a previous step with that tag in outputDatasetTag.",
    )
    parser.add_argument(
        "-S",
        "--site",
        default="T3_US_FNALLPC",
        help="Changes the output site. (Default is T3_US_FNALLPC)",
    )
    parser.add_argument(
        "-d",
        "--dest",
        default="/store/user/",
        help="Changes the output destination path. (Default is /store/user/)",
    )
    parser.add_argument(
        "-a",
        "--pileup",
        default=False,
        help="Generate samples with pileup. (Default is False)",
    )
    parser.add_argument(
        "-C",
        "--conditions",
        default="phase2_realistic_T21",
        help="Conditions option passed to cmsDriver.py. "
        "(Default is phase2_realistic_T21)",
    )
    parser.add_argument(
        "-R",
        "--era",
        default="Phase2C11I13M9",
        help="Era option passed to cmsDriver.py. (Default is Phase2C11I13M9)",
    )
    parser.add_argument(
        "-m",
        "--memory",
        help="Override max memory setting in MB for CRAB. (Default is set by CRAB)",
    )
    parser.add_argument(
        "-N",
        "--cpu",
        type=int,
        help="Override number of cores per job. "
        "(Defaults vary with step and pileup configuration)",
    )
    parser.add_argument(
        "-T",
        "--maxRuntime",
        type=int,
        help="Maximum wall clock time for jobs. (Defaults vary with step)",
    )
    parser.add_argument(
        "--no_exec", action="store_false", help="Prepare scripts but do not submit."
    )
    parser.add_argument(
        "--closeBy",
        action="store_true",
        help="Use CloseByParticleGunProducer instead of Pythia8EGun.",
    )
    parser.add_argument(
        "--maxEn",
        type=float,
        help="Maximum of energy range in case of continuous energy distribution. "
        "(Default is 650 GeV)",
    )
    parser.add_argument(
        "--minEn",
        type=float,
        help="Minimum of energy range in case of continuous energy distribution. "
        "(Default is 0 GeV)",
    )
    parser.add_argument(
        "--maxEta",
        type=float,
        help="Maximum of eta range in case of continuous eta distribution. "
        "(Default is 3.0)",
    )
    parser.add_argument(
        "--minEta",
        type=float,
        help="Minimum of eta range in case of continuous eta distribution. "
        "(Default is 1.5)",
    )
    parser.add_argument(
        "--maxPhi",
        type=float,
        help="Maximum of phi range in case of continuous phi distribution. "
        "(Default is -pi)",
    )
    parser.add_argument(
        "--minPhi",
        type=float,
        help="Minimum of phi range in case of continuous phi distribution. "
        "(Default is pi)",
    )
    parser.add_argument(
        "--nParticles",
        type=int,
        default=1,
        help="Number of particles per event. (Default is 1)",
    )
    parser.add_argument(
        "--delta",
        type=float,
        nargs="*",
        help="Arc distance between two vertices. (Default is 10 cm)",
    )
    parser.add_argument(
        "--beamspot",
        help="Beamspot conditions. (Default is HLLHC or HGCALCloseBy depending on the configuration)",
    )
    parser.add_argument(
        "--overlapping",
        default=False,
        help="If True, particles are shot within delta window. (Default is False)",
    )
    parser.add_argument(
        "--pointing",
        default=True,
        help="If True, particles are shot from (0,0,0). (Default is True)",
    )
    parser.add_argument(
        "--proc", help="Add any process modifiers to the cmsDriver command."
    )

    options = parser.parse_args()

    return options


# Define PDG ID codes
def particleNumbers():
    Dict = {22: "Gamma", 130: "K0L", 11: "E", 111: "Pi0", 211: "PiPlus"}

    return Dict


# Define colors
class col:
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    magenta = "\033[95m"
    blue = "\033[96m"
    endc = "\033[0m"
    bold = "\033[1m"
    uline = "\033[4m"


# Converts floats to nice strings for printouts and names
def makeTag(x):
    tag = str(round(x, 2)).replace(".", "p").replace("-", "minus")
    if re.search("p0$", tag) is not None:
        tag = tag.replace("p0", "")
    return tag


# Append particle, energy, eta and phi tags. Phi tag is skipped if full range is used
# and create printout message.
def tagBuilder(options, p, E, eta, phi, ranges, delta):
    outTag = ""
    printOut = "%s%s" % (col.bold, col.yellow)
    if options.closeBy:
        outTag = "CloseBy"
        printOut = "Using CloseBy gun.\n"
    particleTags = particleNumbers()
    particleTag = particleTags[p]
    if options.nParticles == 1:
        outTag = "%sSingle%s" % (outTag, particleTag)
    elif options.nParticles == 2:
        outTag = "%sDouble%s" % (outTag, particleTag)
    else:
        outTag = "%sMulti%s" % (outTag, particleTag)
    printOut = "%sCreating configuration for %d %s with " % (
        printOut,
        options.nParticles,
        particleTag,
    )
    if E == "notSet":
        outTag = "%s_E%sto%s" % (outTag, makeTag(ranges[0]), makeTag(ranges[1]))
        printOut = "%sE in (%s,%s) GeV, " % (
            printOut,
            makeTag(ranges[0]),
            makeTag(ranges[1]),
        )
    else:
        outTag = "%s_E%s" % (outTag, makeTag(E))
        printOut = "%sE=%s GeV, " % (printOut, makeTag(E))
    if eta == "notSet":
        outTag = "%sEta%sto%s" % (outTag, makeTag(ranges[2]), makeTag(ranges[3]))
        printOut = "%seta in (%s,%s), " % (
            printOut,
            makeTag(ranges[2]),
            makeTag(ranges[3]),
        )
    else:
        outTag = "%sEta%s" % (outTag, makeTag(eta))
        printOut = "%seta=%s, " % (printOut, makeTag(eta))
    if phi == "notSet":
        if options.minPhi is not None or options.maxPhi is not None:
            outTag = "%sPhi%sto%s" % (outTag, makeTag(ranges[4]), makeTag(ranges[5]))
        printOut = "%sand phi in (%s,%s)%s" % (
            printOut,
            makeTag(ranges[4]),
            makeTag(ranges[5]),
            col.endc,
        )
    else:
        outTag = "%sPhi%s" % (outTag, makeTag(phi))
        printOut = "%sand phi=%s%s" % (printOut, makeTag(phi), col.endc)
    if delta != None:
        outTag = "%sDelta%s" % (outTag, makeTag(delta))
    if options.pointing == False:
        outTag = "%sParallel" % (outTag)
    if options.overlapping == True:
        outTag = "%sOverlapping" % (outTag)
    print(printOut)
    return outTag


# Set the particle gun ranges when using discrete values
def setRanges(E, eta, phi, ranges):
    if E != "notSet":
        ranges[0], ranges[1] = E - 0.01, E + 0.01
    if eta != "notSet":
        ranges[2], ranges[3] = eta - 0.01, eta + 0.01
    if phi != "notSet":
        ranges[4], ranges[5] = phi - 0.01, phi + 0.01
    return ranges


# Write CRAB configuration
def writeCRABConfig(
    options, outTag, nThreads, memory, maxRuntime, filein, CMSSW, USER, script
):
    file1 = open("crabConfig_%s_%s.py" % (outTag, options.step), "w")
    requestName = "%s_%s_upgrade2026_%s" % (outTag, CMSSW, options.geometry)
    if options.campaign is not None:
        requestName = "%s_%s" % (requestName, options.campaign)
    outputDatasetTag = requestName
    if options.tag is not None:
        requestName = "%s_%s" % (requestName, options.tag)
    requestName = "'%s_%s'\n" % (requestName, options.step)
    outputDatasetTag = "'%s_%s'\n\n" % (outputDatasetTag, options.step)
    file1.write("# Script automatically generated by submit.py\n\n")
    file1.write("from CRABClient.UserUtilities import config\n")
    file1.write("config = config()\n")
    file1.write("config.General.requestName = %s" % requestName)
    file1.write("config.General.workArea = 'crab_projects'\n")
    file1.write("config.General.transferOutputs = True\n\n")
    file1.write("config.JobType.psetName = '%s'\n" % (script))
    file1.write("config.JobType.maxMemoryMB = %d\n" % memory)
    file1.write("config.JobType.numCores = %d\n" % nThreads)
    file1.write("config.JobType.maxJobRuntimeMin = %d\n\n" % maxRuntime)
    file1.write("config.Data.unitsPerJob = %d\n" % options.unitsPerJob)
    file1.write("config.Data.outLFNDirBase = '%s%s/'\n" % (options.dest, USER))
    file1.write("config.Data.outputDatasetTag = %s" % (outputDatasetTag))
    file1.write("config.Site.storageSite = '%s'\n" % options.site)
    file1.write("config.Site.blacklist = ['T2_US_Caltech']\n\n")
    file1.write("# Step-specific parameters\n")
    if options.step == "step1":
        file1.write("config.General.transferLogs = False\n")
        file1.write("config.JobType.pluginName = 'PrivateMC'\n")
        file1.write("config.Data.outputPrimaryDataset = '%s'\n" % outTag)
        file1.write("config.Data.splitting = 'EventBased'\n")
        file1.write("NJOBS = %d\n" % options.njobs)
        file1.write("config.Data.totalUnits = config.Data.unitsPerJob * NJOBS\n")
    else:
        file1.write("config.General.transferLogs = True\n")
        file1.write("config.JobType.pluginName = 'Analysis'\n")
        file1.write("config.Data.inputDataset = '%s'\n" % filein)
        file1.write("config.Data.inputDBS = 'phys03'\n")
        file1.write("config.Data.splitting = 'FileBased'\n")
        file1.write("config.Data.totalUnits = %d\n" % options.njobs)
    if options.step == "ntuples":
        file1.write("config.Data.publication = False\n\n")
    else:
        file1.write("config.Data.publication = True\n\n")


def fetchData(options, energy, particle, eta, phi, ranges, delta, CMSSW, user):
    # Primary dataset
    primary = tagBuilder(options, particle, energy, eta, phi, ranges, delta)

    # output dataset
    output = "%s_%s_upgrade2026_%s" % (primary, CMSSW, options.geometry)
    if options.campaign is not None:
        output = "%s_%s" % (output, options.campaign)

    # Attach step to secondary
    if options.step == "step2":
        output = "%s_step1" % (output)
    elif options.step == "step3":
        output = "%s_step2" % (output)
    elif options.step == "ntuples":
        output = "%s_step3" % (output)
    else:
        raise ValueError("Unknown step:%s" % options.step)

    # dasgoclient command
    query = "dataset dataset=/%s/%s-%s-*/USER instance=prod/phys03" % (
        primary,
        user,
        output,
    )

    print('Executing: dasgoclient -query="%s' % (query))
    result = subprocess.run(["dasgoclient", "-query", query], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")


def extractCMSSWversion(cmssw):
    # Check for nightly build version
    if cmssw.find("_X_") > -1:
        print(
            "%sWarning%s: using a nightly CMSSW build! Version comparisons might yield incorrect results!"
        )
        cmssw = cmssw[: cmssw.find("_X_")]
        cmssw = cmssw + "_0_0"
    # Convert to X_Y_Z_A format. Prereleases get a minus sign
    if cmssw.find("pre") == -1 and cmssw.find("patch") == -1:
        cmssw = cmssw + "_0"
    cmssw = cmssw.strip("CMSSW_").replace("pre", "-").replace("patch", "")
    # Extract the numbers
    version = []
    while cmssw != "":
        i = cmssw.find("_")
        if i > -1:
            version.append(int(cmssw[0:i]))
            cmssw = cmssw[i + 1 :]
        else:
            version.append(int(cmssw))
            cmssw = ""
    return version


def compareCMSSWversions(cmssw1, cmssw2):
    """
    Input: (cmssw1, cmssw2) -> CMSSW versions in CMSSW_X_Y_Z(...) format.
    Returns:
        *  1 if cmssw1  > cmssw2
        *  0 if cmssw1 == cmssw2
        * -1 if cmssw1  < cmssw2
    """
    # Extract version numbers
    cmssw1 = extractCMSSWversion(cmssw1)
    cmssw2 = extractCMSSWversion(cmssw2)
    # Make sure the comparison is valid for two prereleases
    if len(cmssw1) == 4 and len(cmssw2) == 4 and cmssw1[3] < 0 and cmssw2[3] < 0:
        cmssw1[3] = abs(cmssw1[3])
        cmssw2[3] = abs(cmssw2[3])
    # Comparison loop
    result = 0
    i = 0
    maxI = min(len(cmssw1), len(cmssw2))
    while not result and i < maxI:
        if cmssw1[i] > cmssw2[i]:
            result = 1
        elif cmssw1[i] < cmssw2[i]:
            result = -1
        i += 1
    return result
