#
#  Author: Christos Papageorgakis
#
# Contains option parsing definitions
#

import argparse

def standardParser():
    parser = argparse.ArgumentParser(description='Utility for managing multiple CRAB3 submissions.',usage='%(prog)s [options]')
    parser.add_argument('-s','--step', help='Step to be used.',choices=['step1','step2','step3','ntuples'],required=True)
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging. (Default is D54)',default='D54')
    parser.add_argument('-E','--energies',type=int, help='List of energies to shoot.',nargs='*')
    parser.add_argument('-e','--eta',type=string, help='List of eta to shoot.',nargs='*')
    parser.add_argument('-p','--particles',type=int, help='List of particles to shoot',nargs='*')
    parser.add_argument('-t','--tag', help='Unique tag to discern between different submissions.')

    options = parser.parse_args()

    return options

def mainParserStep1():
    parser = argparse.ArgumentParser(description='Submit multiple step1 jobs with CRAB3.',usage='%(prog)s [options]')
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging. (Default is D54)',default='D54')
    parser.add_argument('-n','--njobs',type=int, help='Number of jobs to run.',required=True)
    parser.add_argument('-u','--unitsPerJob',type=int, help='Events per job.',required=True)
    parser.add_argument('-E','--energies',type=int, help='List of energies to shoot.',nargs='*')
    parser.add_argument('-e','--eta',type=string, help='List of eta to shoot.',nargs='*')
    parser.add_argument('-p','--particles',type=int, help='List of particles to shoot',nargs='*')
    parser.add_argument('-t','--tag', help='Unique tag to discern between different submissions.')

    options = parser.parse_args()

    return options

def mainParserStepN():
    parser = argparse.ArgumentParser(description='Submit multiple simulation jobs with CRAB3',usage='%(prog)s [options]')
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging. (Default is D54)',default='D54')
    parser.add_argument('-n','--njobs',type=int, help='Number of jobs to run.',required=True)
    parser.add_argument('-u','--unitsPerJob',type=int, help='Number of files to use per job.',required=True)
    parser.add_argument('-E','--energies',type=int,help='List of energies to shoot.',nargs='*')
    parser.add_argument('-e','--eta',type=string, help='List of eta to shoot.',nargs='*')
    parser.add_argument('-p','--particles',type=int, help='List of particles to shoot',nargs='*')
    parser.add_argument('-t','--tag', help='Unique tag to discern between different submissions.')

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
