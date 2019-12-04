#
#  Author: Christos Papageorgakis
#
# Contains option parsing definitions
#

import argparse

def standardParser():
    parser = argparse.ArgumentParser(description='Scripts configuration',usage='%(prog)s [options]')
    parser.add_argument('-s','--step', help='Step to be used.',choices=['step1','step2','step3','ntuple'],required=True)
    parser.add_argument('-g','--geometry', help='Detector geometry for tagging.',default='D41')

    options = parser.parse_args()

    return options
