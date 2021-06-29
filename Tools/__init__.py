#
#  Author: Christos Papageorgakis
#
# Contains option parsing definitions
#

import argparse

def mainParserStep1():
    parser = argparse.ArgumentParser(description='Submit multiple step1 jobs with CRAB3.',usage='%(prog)s [options]')
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging. (Default is D76)',default='D76')
    parser.add_argument('-n','--njobs',type=int, help='Number of jobs to run.',required=True)
    parser.add_argument('-u','--unitsPerJob',type=int, help='Events per job.',required=True)
    parser.add_argument('-E','--energies',type=int, help='List of energies to shoot.',nargs='*')
    parser.add_argument('-e','--eta', help='List of eta to shoot.',nargs='*')
    parser.add_argument('-P','--phi', help='List of phi to shoot.',nargs='*')
    parser.add_argument('-p','--particles',type=int, help='List of particles to shoot.',nargs='*')
    parser.add_argument('-t','--tag', help='Unique tag to discern between different submissions.',default=None)
    parser.add_argument('-c','--campaign', help='Adds a tag to outputDatasetTag.',default=None)
    parser.add_argument('-S','--site', help='Changes the output site. (Default is T3_US_FNALLPC)',default='T3_US_FNALLPC')
    parser.add_argument('-d','--dest', help='Changes the output destination path. (Default is /store/user/)',default='/store/user/')
    parser.add_argument('-a','--pileup', help='Generate samples with pileup. (Default is False)',default=False)
    parser.add_argument('-C','--conditions', help='Conditions option passed to cmsDriver.py. (Default is phase2_realistic_T21)',default='phase2_realistic_T21')
    parser.add_argument('-R','--era', help='Era option passed to cmsDriver.py. (Default is Phase2C11I13M9)',default='Phase2C11I13M9')
    parser.add_argument('--no_exec', help='Prepare scripts but do not submit.',action='store_false')
    parser.add_argument('--closeBy', help='Use CloseByParticleGunProducer instead of Pythia8EGun.',action='store_true')

    options = parser.parse_args()

    return options

def mainParserStepN():
    parser = argparse.ArgumentParser(description='Submit multiple simulation jobs with CRAB3',usage='%(prog)s [options]')
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging. (Default is D76)',default='D76')
    parser.add_argument('-n','--njobs',type=int, help='Number of jobs to run.',required=True)
    parser.add_argument('-u','--unitsPerJob',type=int, help='Number of files to use per job.',required=True)
    parser.add_argument('-E','--energies',type=int,help='List of energies to shoot.',nargs='*')
    parser.add_argument('-e','--eta', help='List of eta to shoot.',nargs='*')
    parser.add_argument('-P','--phi', help='List of phi to shoot.',nargs='*')
    parser.add_argument('-p','--particles',type=int, help='List of particles to shoot.',nargs='*')
    parser.add_argument('-t','--tag', help='Unique tag to discern between different submissions.',default=None)
    parser.add_argument('-c','--campaign', help='Adds a tag to outputDatasetTag.',default=None)
    parser.add_argument('-S','--site', help='Changes the output site. (Default is T3_US_FNALLPC)',default='T3_US_FNALLPC')
    parser.add_argument('-d','--dest', help='Changes the output destination path. (Default is /store/user/)',default='/store/user/')
    parser.add_argument('-a','--pileup', help='Generate samples with pileup.',default=False)
    parser.add_argument('-C','--conditions', help='Conditions option passed to cmsDriver.py. (Default is phase2_realistic_T21)',default='phase2_realistic_T21')
    parser.add_argument('-R','--era', help='Era option passed to cmsDriver.py. (Default is Phase2C11I13M9)',default='Phase2C11I13M9')
    parser.add_argument('--no_exec', help='Prepare scripts but do not submit.',action='store_false')
    parser.add_argument('--closeBy', help='Use CloseByParticleGunProducer instead of Pythia8EGun.',action='store_true')

    options = parser.parse_args()

    return options

def particleNumbers():
    Dict = {
        22: 'Gamma',
        130: 'K0L',
        11: 'E',
        111: 'Pi0',
        211: 'PiPlus'
    }

    return Dict

class col:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    magenta = '\033[95m'
    blue = '\033[96m'
    endc = '\033[0m'
    bold = '\033[1m'
    uline = '\033[4m'
