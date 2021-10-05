#
#  Author: Christos Papageorgakis
#
# Contains option parsing definitions
# and other necessary tools.
#

import os, argparse, re

def mainParser():
    parser = argparse.ArgumentParser(description='Submit and manage multiple particle gun jobs with CRAB3.',
                                     usage='%(prog)s [options]')
    parser.add_argument('-s', '--step', choices=['step1','step2','step3','ntuples'], required=True,
                        help='Step to be used.')
    parser.add_argument('-g', '--geometry', default='D76',
                        help='Detector geometry for tagging. (Default is D76)')
    parser.add_argument('-n', '--njobs', type=int, default=10,
                        help='Number of jobs to run. (Default is 10)')
    parser.add_argument('-u', '--unitsPerJob', type=int, default=10,
                        help='Events per job for step1 and files processed per '
                             'job for all other steps. (Default is 10)')
    parser.add_argument('-E', '--energies', type=float, nargs='*',
                        help='List of energies to shoot.')
    parser.add_argument('-e', '--eta', type=float, nargs='*',
                        help='List of eta to shoot.')
    parser.add_argument('-P', '--phi', type=float, nargs='*',
                        help='List of phi to shoot.')
    parser.add_argument('-p', '--particles', type=int, nargs='*',
                        help='List of particles to shoot.')
    parser.add_argument('-t', '--tag',
                        help='Unique tag to discern between different submissions.')
    parser.add_argument('-i', '--inputTag',
                        help='Tag of input dataset.')
    parser.add_argument('-c', '--campaign',
                        help='Adds a tag to outputDatasetTag.')
    parser.add_argument('-S', '--site', default='T3_US_FNALLPC',
                        help='Changes the output site. (Default is T3_US_FNALLPC)')
    parser.add_argument('-d', '--dest', default='/store/user/',
                        help='Changes the output destination path. (Default is /store/user/)')
    parser.add_argument('-a', '--pileup', default=False,
                        help='Generate samples with pileup. (Default is False)')
    parser.add_argument('-C', '--conditions', default='phase2_realistic_T21',
                        help='Conditions option passed to cmsDriver.py. '
                             '(Default is phase2_realistic_T21)')
    parser.add_argument('-R', '--era', default='Phase2C11I13M9',
                        help='Era option passed to cmsDriver.py. (Default is Phase2C11I13M9)')
    parser.add_argument('-m', '--memory',
                        help='Override max memory setting in MB for CRAB. (Default is set by CRAB)')
    parser.add_argument('-N', '--cpu', type=int,
                        help='Override number of cores per job. '
                             '(Defaults vary with step and pileup configuration)')
    parser.add_argument('-T', '--maxRuntime', type=int,
                        help='Maximum wall clock time for jobs. (Defaults vary with step)')
    parser.add_argument('--no_exec', action='store_false',
                        help='Prepare scripts but do not submit.')
    parser.add_argument('--closeBy', action='store_true',
                        help='Use CloseByParticleGunProducer instead of Pythia8EGun.')
    parser.add_argument('--maxEn', type=float,
                        help='Maximum of energy range in case of continuous energy distribution. '
                             '(Default is 650 GeV)')
    parser.add_argument('--minEn', type=float,
                        help='Minimum of energy range in case of continuous energy distribution. '
                             '(Default is 0 GeV)')
    parser.add_argument('--maxEta', type=float,
                        help='Maximum of eta range in case of continuous eta distribution. '
                             '(Default is 3.0)')
    parser.add_argument('--minEta', type=float,
                        help='Minimum of eta range in case of continuous eta distribution. '
                             '(Default is 1.5)')
    parser.add_argument('--maxPhi', type=float,
                        help='Maximum of phi range in case of continuous phi distribution. '
                             '(Default is -pi)')
    parser.add_argument('--minPhi', type=float,
                        help='Minimum of phi range in case of continuous phi distribution. '
                             '(Default is pi)')
    parser.add_argument('--nParticles', type=int, default=1,
                        help='Number of particles per event. (Default is 1)')
    parser.add_argument('--delta', type=float, nargs='*',
                        help='Arc distance between two vertices. (Default is 10 cm)')
    parser.add_argument('--overlapping', default=False,
                        help='If True, particles are shot within delta window. (Default is False)')
    parser.add_argument('--pointing', default=True,
                        help='If True, particles are shot from (0,0,0). (Default is True)')
    parser.add_argument('--proc',
                        help='Add any process modifiers to the cmsDriver command.')

    options = parser.parse_args()

    return options

# Define PDG ID codes
def particleNumbers():
    Dict = {
        22: 'Gamma',
        130: 'K0L',
        11: 'E',
        111: 'Pi0',
        211: 'PiPlus'
    }

    return Dict

# Define colors
class col:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    magenta = '\033[95m'
    blue = '\033[96m'
    endc = '\033[0m'
    bold = '\033[1m'
    uline = '\033[4m'

# Converts floats to nice strings for printouts and names
def makeTag(x):
    tag = str(round(x,2)).replace(".","p").replace("-","minus")
    if re.search("p0$",tag) is not None:
        tag = tag.replace("p0","")
    return tag

# Append particle, energy, eta and phi tags. Phi tag is skipped if full range is used
# and create printout message.
def tagBuilder(options, p, E, eta, phi, ranges, delta):
    outTag = ''
    printOut = '%s%s'%(col.bold, col.yellow)
    if options.closeBy:
        outTag = 'CloseBy'
        printOut = 'Using CloseBy gun.\n'
    particleTags = particleNumbers()
    particleTag = particleTags[p]
    if options.nParticles == 1:
        outTag = '%sSingle%s'%(outTag,particleTag)
    elif options.nParticles == 2:
        outTag = '%sDouble%s'%(outTag,particleTag)
    else:
        outTag = '%sMulti%s'%(outTag,particleTag)
    printOut = '%sCreating configuration for %d %s with '%(printOut,options.nParticles,particleTag)
    if E == 'notSet':
        outTag = '%s_E%sto%s'%(outTag,makeTag(ranges[0]),makeTag(ranges[1]))
        printOut = '%sE in (%s,%s) GeV, '%(printOut,makeTag(ranges[0]),makeTag(ranges[1]))
    else:
        outTag = '%s_E%s'%(outTag,makeTag(E))
        printOut = '%sE=%s GeV, '%(printOut,makeTag(E))
    if eta == 'notSet':
        outTag = '%sEta%sto%s'%(outTag,makeTag(ranges[2]),makeTag(ranges[3]))
        printOut = '%seta in (%s,%s), '%(printOut,makeTag(ranges[2]),makeTag(ranges[3]))
    else:
        outTag = '%sEta%s'%(outTag,makeTag(eta))
        printOut = '%seta=%s, '%(printOut,makeTag(eta))
    if phi == 'notSet':
        if options.minPhi is not None or options.maxPhi is not None:
            outTag = '%sPhi%sto%s'%(outTag,makeTag(ranges[4]),makeTag(ranges[5]))
        printOut = '%sand phi in (%s,%s)%s'%(printOut,makeTag(ranges[4]),makeTag(ranges[5]),col.endc)
    else:
        outTag = '%sPhi%s'%(outTag,makeTag(phi))
        printOut = '%sand phi=%s%s'%(printOut,makeTag(phi),col.endc)
    if delta != None:
        outTag = '%sDelta%s'%(outTag,makeTag(delta))
    if options.pointing == False:
        outTag = '%sParallel'%(outTag)
    if options.overlapping == True:
        outTag = '%sOverlapping'%(outTag)
    print(printOut)
    return outTag

# Set the particle gun ranges when using discrete values
def setRanges(E, eta, phi, ranges):
    if E != 'notSet':
        ranges[0], ranges[1] = E-0.01, E+0.01
    if eta != 'notSet':
        ranges[2], ranges[3] = eta-0.01, eta+0.01
    if phi != 'notSet':
        ranges[4], ranges[5] = phi-0.01, phi+0.01
    return ranges

# Write CRAB configuration
def writeCRABConfig(options, outTag, nThreads, memory, maxRuntime, filein, CMSSW, USER, script):
    file1 = open('crabConfig_%s_%s.py'%(outTag,options.step),'w')
    requestName = "%s_%s_upgrade2026_%s"%(outTag,CMSSW,options.geometry)
    if options.campaign is not None:
        requestName = "%s_%s"%(requestName,options.campaign)
    outputDatasetTag = requestName
    if options.tag is not None:
        requestName = "%s_%s"%(requestName,options.tag)
    requestName = "'%s_%s'\n"%(requestName,options.step)
    outputDatasetTag = "'%s_%s'\n\n"%(outputDatasetTag,options.step)
    file1.write('# Script automatically generated by submit.py\n\n')
    file1.write('from CRABClient.UserUtilities import config\n')
    file1.write('config = config()\n')
    file1.write("config.General.requestName = %s"%(requestName))
    file1.write("config.General.workArea = 'crab_projects'\n")
    file1.write("config.General.transferOutputs = True\n\n")
    file1.write("config.JobType.psetName = '%s'\n"%(script))
    file1.write("config.JobType.maxMemoryMB = %d\n"%memory)
    file1.write("config.JobType.numCores = %d\n"%nThreads)
    file1.write("config.JobType.maxJobRuntimeMin = %d\n\n"%maxRuntime)
    file1.write("config.Data.unitsPerJob = %d\n"%options.unitsPerJob)
    file1.write("config.Data.outLFNDirBase = '%s%s/'\n"%(options.dest,USER))
    file1.write("config.Data.outputDatasetTag = %s"%(outputDatasetTag))
    file1.write("config.Site.storageSite = '%s'\n"%options.site)
    file1.write("config.Site.blacklist = ['T2_US_Caltech']\n\n")
    file1.write("# Step-specific parameters\n")
    if options.step == 'step1':
        file1.write("config.General.transferLogs = False\n")
        file1.write("config.JobType.pluginName = 'PrivateMC'\n")
        file1.write("config.Data.outputPrimaryDataset = '%s'\n"%outTag)
        file1.write("config.Data.splitting = 'EventBased'\n")
        file1.write("NJOBS = %d\n"%options.njobs)
        file1.write("config.Data.totalUnits = config.Data.unitsPerJob * NJOBS\n")
    else:
        file1.write("config.General.transferLogs = True\n")
        file1.write("config.JobType.pluginName = 'Analysis'\n")
        file1.write("config.Data.inputDataset = '%s'\n"%((filein.readline())[:-1]))
        file1.write("config.Data.inputDBS = 'phys03'\n")
        file1.write("config.Data.splitting = 'FileBased'\n")
        file1.write("config.Data.totalUnits = %d\n"%options.njobs)
    if options.step == 'ntuples':
        file1.write("config.Data.publication = False\n\n")
    else:
        file1.write("config.Data.publication = True\n\n")

def fetchData(options, energies, particles, etas, phis, ranges):
    # Initialize the command
    command = 'python checkStatus.py'

    # Attach step option
    if options.step == 'step2':
        command = '%s -s step1'%(command)
    elif options.step == 'step3':
        command = '%s -s step2'%(command)
    elif options.step == 'ntuples':
        command = '%s -s step3'%(command)
    else:
        raise ValueError('Unknown step:%s'%options.step)

    # Attach particle option
    pList = ' -p'
    for p in particles:
        pList = '%s %d'%(pList,p)
    command = '%s%s'%(command, pList)

    # Attach energy options
    enList = ' -E'
    for E in energies:
        if E == 'notSet':
            enList = ''
        else:
            enList = '%s %f'%(enList,E)
    command = '%s%s'%(command, enList)
    if options.minEn is not None:
        command = '%s --minEn %f'%(command,ranges[0])
    if options.maxEn is not None:
        command = '%s --maxEn %f'%(command,ranges[1])

    # Attach eta options
    etaList = ' -e'
    for eta in etas:
        if eta == 'notSet':
            etaList = ''
        else:
            etaList = '%s %f'%(etaList,eta)
    command = '%s%s'%(command, etaList)
    if options.minEta is not None:
        command = '%s --minEta %f'%(command,ranges[2])
    if options.maxEta is not None:
        command = '%s --maxEta %f'%(command,ranges[3])

    # Attach phi options
    phiList = ' -P'
    for phi in phis:
        if phi == 'notSet':
            phiList = ''
        else:
            phiList = '%s %f'%(phiList,phi)
    command = '%s%s'%(command, phiList)
    if options.minPhi is not None:
        command = '%s --minPhi %f'%(command,ranges[4])
    if options.maxPhi is not None:
        command = '%s --maxPhi %f'%(command,ranges[5])

    # Attach tag option
    if options.inputTag is not None:
        command = '%s -t %s'%(command,options.inputTag)
    elif options.tag is not None:
        command = '%s -t %s'%(command,options.tag)

    # Attach campaign option
    if options.campaign is not None:
        command = '%s -c %s'%(command,options.campaign)

    # Attach closeBy option
    if options.closeBy:
        command = '%s --closeBy'%(command)

    # Attach closeBy-related options
    if options.nParticles is not None:
        command = '%s --nParticles %d'%(command,options.nParticles)

    if options.delta is not None:
        deltaList = ' --delta'
        for delta in options.delta:
            deltaList = '%s %f'%(deltaList,delta)
        command = '%s%s'%(command, deltaList)

    if options.overlapping:
        command = '%s --overlapping'%(command)
    if options.pointing is not True:
        command = '%s --pointing'%(command)

    print("Executing: %s"%(command))
    os.system("sh Tools/createList.sh '%s'"%(command))
