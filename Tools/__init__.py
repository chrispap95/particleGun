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

    options = parser.parse_args()

    return options

def mainParserStep1():
    parser = argparse.ArgumentParser(description='Scripts configuration.',usage='%(prog)s [options]')
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging.',default='D41')
    parser.add_argument('-n','--njobs', help='Number of jobs to run.',required=True)
    parser.add_argument('-u','--unitsPerJob', help='Events per job.',required=True)
    options = parser.parse_args()

    return options

def mainParserStepN():
    parser = argparse.ArgumentParser(description='Scripts configuration',usage='%(prog)s [options]')
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging.',default='D41')
    parser.add_argument('-n','--njobs', help='Number of jobs to run.',required=True)
    parser.add_argument('-u','--unitsPerJob', help='Number of files to use per job.',required=True)
    options = parser.parse_args()

    return options
