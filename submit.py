import os
import sys

from Scripts import ntuples, step1, step2, step3
from Tools import mainParser

sys.path.append(os.path.abspath(os.path.curdir))

def submit(options):
    if options.step == "step1":
        step1.step1(options)
    elif options.step == "step2":
        step2.step2(options)
    elif options.step == "step3":
        step3.step3(options)
    elif options.step == "ntuples":
        ntuples.ntuples(options)
    else:
        raise ValueError(f"Unknown step '{options.step}'")

if __name__ == "__main__":
    options = mainParser()
    submit(options)