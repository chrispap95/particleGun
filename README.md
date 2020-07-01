# particleGun ![Python application](https://github.com/chrispap95/particleGun/workflows/Python%20application/badge.svg)
Scripts for easy and multiple MC samples generation.

## Instructions
To clone the code just do
```bash
wget https://raw.githubusercontent.com/chrispap95/particleGun/master/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_11_2_0_pre1
cd CMSSW_11_2_0_pre1/src
cmsenv
cd particleGun
```

The setup.sh script is going to take care setting up a CMSSW release and cloning
the necessary repositories. (CVMFS access is needed)

Submit step1 (GEN-SIM) by issuing:
```bash
python step1.py -E 5 10 15 -e 1p7 -p 22 -n 10 -u 50
```
That is going to submit single gamma (```-p 22```) at energies 5, 10, 15 GeV (```-E 5 10 15```) and eta 1.7 (```-e 1p7```). For each energy and eta, the script submits 10 jobs (```-n 10```) with 50 events each (```-u 50```). To see the options available:
```bash
[chpapage@cmslpc163 particleGun]$ python step1.py --help
usage: step1.py [options]

Submit multiple step1 jobs with CRAB3.

optional arguments:
  -h, --help            show this help message and exit
  -g GEOMETRY, --geometry GEOMETRY
                        Detector geometry for tagging. (Default is D54)
  -n NJOBS, --njobs NJOBS
                        Number of jobs to run.
  -u UNITSPERJOB, --unitsPerJob UNITSPERJOB
                        Events per job.
  -E [ENERGIES [ENERGIES ...]], --energies [ENERGIES [ENERGIES ...]]
                        List of energies to shoot.
  -e [ETA [ETA ...]], --eta [ETA [ETA ...]]
                        List of eta to shoot.
  -P [PHI [PHI ...]], --phi [PHI [PHI ...]]
                        List of phi to shoot.
  -p [PARTICLES [PARTICLES ...]], --particles [PARTICLES [PARTICLES ...]]
                        List of particles to shoot.
  -t TAG, --tag TAG     Unique tag to discern between different submissions.
  --no_exec             Prepare scripts but do not submit.
  --closeBy             Use CloseByParticleGunProducer instead of Pythia8EGun.
```

To check the submitted jobs issue:
```bash
python checkStatus.py -s step1 -E 5 10 15 -e 1p7 -p 22
```

Similarly, to resubmit failed jobs or kill them:
```bash
python resubmit.py -s step1 -E 5 10 15 -e 1p7 -p 22
```
and
```bash
python killEmAll.py -s step1 -E 5 10 15 -e 1p7 -p 22
```

You can check the produced datasets online at https://cmsweb.cern.ch/das/ by searching for the dataset name from the output of checkStatus.py.

To submit step2:
```bash
python step2.py -E 5 10 15 -e 1p7 -p 22 -n 10 -u 1
```
and step3:
```bash
python step3.py -E 5 10 15 -e 1p7 -p 22 -n 10 -u 1
```

Finally, if you want to produced ntuples (they can't be published) do:
```bash
python ntuples.py -E 5 10 15 -e 1p7 -p 22 -n 10 -u 1
```
