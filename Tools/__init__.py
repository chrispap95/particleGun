#
#  Author: Christos Papageorgakis
#
# Contains option parsing definitions
# and other necessary tools.
#

import argparse

def mainParser():
    parser = argparse.ArgumentParser(description='Submit and manage multiple particle gun jobs with CRAB3.',
                                     usage='%(prog)s [options]')
    parser.add_argument('-s', '--step', choices=['step1','step2','step3','ntuples'], required=True,
                        help='Step to be used.')
    parser.add_argument('-g', '--geometry', default='D76',
                        help='Detector geometry for tagging. (Default is D76)')
    parser.add_argument('-n', '--njobs', type=int, default='10',
                        help='Number of jobs to run. (Default is 10)')
    parser.add_argument('-u', '--unitsPerJob', type=int, default='10',
                        help='Events per job for step1 and files processed per job for all other steps. '
                             '(Default is 10)')
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
                        help='Override number of cores per job. (Default is 1)')
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
