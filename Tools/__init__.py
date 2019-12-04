#
#  Author: Christos Papageorgakis
#
# Contains option parsing definitions
#

import argparse

def standardParser():
    parser = argparse.ArgumentParser(description='Scripts configuration.',usage='%(prog)s [options]')
    parser.add_argument('-s','--step', help='Step to be used.',choices=['step1','step2','step3','ntuple'],required=True)
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging.',default='D41')
    parser.add_argument('-E','--energies',type=int, help='List of energies to shoot.',nargs='*')
    parser.add_argument('-e','--eta', help='List of eta to shoot.',nargs='*')
    parser.add_argument('-p','--particles', help='List of particles to shoot',nargs='*')
 
    options = parser.parse_args()

    return options

def mainParserStep1():
    parser = argparse.ArgumentParser(description='Scripts configuration.',usage='%(prog)s [options]')
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging.',default='D41')
    parser.add_argument('-n','--njobs', help='Number of jobs to run.',required=True)
    parser.add_argument('-u','--unitsPerJob', help='Events per job.',required=True)
    parser.add_argument('-E','--energies',type=int, help='List of energies to shoot.',nargs='*')
    parser.add_argument('-e','--eta', help='List of eta to shoot.',nargs='*')
    parser.add_argument('-p','--particles', help='List of particles to shoot',nargs='*')

    options = parser.parse_args()

    return options

def mainParserStepN():
    parser = argparse.ArgumentParser(description='Scripts configuration',usage='%(prog)s [options]')
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging.',default='D41')
    parser.add_argument('-n','--njobs', help='Number of jobs to run.',required=True)
    parser.add_argument('-u','--unitsPerJob', help='Number of files to use per job.',required=True)
    parser.add_argument('-E','--energies',type=int,help='List of energies to shoot.',nargs='*')
    parser.add_argument('-e','--eta', help='List of eta to shoot.',nargs='*')
    parser.add_argument('-p','--particles', help='List of particles to shoot',nargs='*')

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
