# particleGun ![Python application](https://github.com/chrispap95/particleGun/workflows/Python%20application/badge.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Massive parallel MC sample generation submission handling for particle gun cases (designed for HGCAL workflows). This package will automate loops over multiple energies, η, φ, particle types, etc. Continuous ranges can be used as well for some of the input parameters.

## Instructions

To clone the code just do

```bash
wget https://raw.githubusercontent.com/chrispap95/particleGun/master/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_11_3_1_patch1
cd CMSSW_11_3_1_patch1/src
cmsenv
cd particleGun
```

The setup.sh script is going to take care setting up a CMSSW release and cloning
the necessary repositories. (CVMFS access is needed)

The repository contains four scripts that can be used to submit, check, resubmit and kill particle gun jobs.

Submit step1 (GEN-SIM) by issuing:

```bash
python submit.py -s step1 -E 5 10 15 -e 1.62 -p 22 -n 10 -u 50 -c campaign1 -t tag1
```

This command will submit step1 jobs (`-s step1`) single gamma (`-p 22`) at energies 5, 10, 15 GeV (`-E 5 10 15`) and eta 1.7 (`-e 1.62`). For each energy and eta, the script submits 10 jobs (`-n 10`) with 50 events each (`-u 50`). Campaign and tag arguments are used for bookmarking purposes.

If you want to shoot at a continuous range of energies, eta or phi, then omit the `-E`, `-e`, and `-P` options, respectively, and use the `--maxEn`, `minEn`, etc options to define the desired ranges.

To see the options available:

```
usage: submit.py [options]

Submit and manage multiple particle gun jobs with CRAB3.

optional arguments:
  -h, --help            show this help message and exit
  -s {step1,step2,step3,ntuples}, --step {step1,step2,step3,ntuples}
                        Step to be used.
  -g GEOMETRY, --geometry GEOMETRY
                        Detector geometry for tagging. (Default is D76)
  -n NJOBS, --njobs NJOBS
                        Number of jobs to run. (Default is 10)
  -u UNITSPERJOB, --unitsPerJob UNITSPERJOB
                        Events per job for step1 and files processed per job for all other steps. (Default is 10)
  -E [ENERGIES ...], --energies [ENERGIES ...]
                        List of energies to shoot.
  -e [ETA ...], --eta [ETA ...]
                        List of eta to shoot.
  -P [PHI ...], --phi [PHI ...]
                        List of phi to shoot.
  -p [PARTICLES ...], --particles [PARTICLES ...]
                        List of particles to shoot.
  -t TAG, --tag TAG     Unique tag to discern between different submissions.
  -i INPUTTAG, --inputTag INPUTTAG
                        Tag of input dataset.
  -c CAMPAIGN, --campaign CAMPAIGN
                        Adds a tag to outputDatasetTag.
  --inputCampaign INPUTCAMPAIGN
                        Searches for a previous step with that tag in outputDatasetTag.
  -S SITE, --site SITE  Changes the output site. (Default is T3_US_FNALLPC)
  -d DEST, --dest DEST  Changes the output destination path. (Default is /store/user/)
  -a PILEUP, --pileup PILEUP
                        Generate samples with pileup. (Default is False)
  -C CONDITIONS, --conditions CONDITIONS
                        Conditions option passed to cmsDriver.py. (Default is phase2_realistic_T21)
  -R ERA, --era ERA     Era option passed to cmsDriver.py. (Default is Phase2C11I13M9)
  -m MEMORY, --memory MEMORY
                        Override max memory setting in MB for CRAB. (Default is set by CRAB)
  -N CPU, --cpu CPU     Override number of cores per job. (Defaults vary with step and pileup configuration)
  -T MAXRUNTIME, --maxRuntime MAXRUNTIME
                        Maximum wall clock time for jobs. (Defaults vary with step)
  --no_exec             Prepare scripts but do not submit.
  --closeBy             Use CloseByParticleGunProducer instead of Pythia8EGun.
  --maxEn MAXEN         Maximum of energy range in case of continuous energy distribution. (Default is 650 GeV)
  --minEn MINEN         Minimum of energy range in case of continuous energy distribution. (Default is 0 GeV)
  --maxEta MAXETA       Maximum of eta range in case of continuous eta distribution. (Default is 3.0)
  --minEta MINETA       Minimum of eta range in case of continuous eta distribution. (Default is 1.5)
  --maxPhi MAXPHI       Maximum of phi range in case of continuous phi distribution. (Default is -pi)
  --minPhi MINPHI       Minimum of phi range in case of continuous phi distribution. (Default is pi)
  --nParticles NPARTICLES
                        Number of particles per event. (Default is 1)
  --delta [DELTA ...]   Arc distance between two vertices. (Default is 10 cm)
  --beamspot BEAMSPOT   Beamspot conditions. (Default is HLLHC or HGCALCloseBy depending on the configuration)
  --overlapping OVERLAPPING
                        If True, particles are shot within delta window. (Default is False)
  --pointing POINTING   If True, particles are shot from (0,0,0). (Default is True)
  --proc PROC           Add any process modifiers to the cmsDriver command.
```

To check the submitted jobs issue:

```bash
python checkStatus.py -s step1 -E 5 10 15 -e 1.62 -p 22 -c campaign1 -t tag1
```

Similarly, to resubmit failed jobs or kill them:

```bash
python resubmit.py -s step1 -E 5 10 15 -e 1.62 -p 22 -c campaign1 -t tag1
```

and

```bash
python killEmAll.py -s step1 -E 5 10 15 -e 1.62 -p 22 -c campaign1 -t tag1
```

You can check the produced datasets online at https://cmsweb.cern.ch/das/ by searching for the dataset name from the output of checkStatus.py.

To submit step2:

```bash
python submit.py -s step2 -E 5 10 15 -e 1.62 -p 22 -n 10 -u 1 -c campaign1 -i tag1 -t tag1
```

and step3:

```bash
python submit.py -s step3 -E 5 10 15 -e 1.62 -p 22 -n 10 -u 1 -c campaign1 -i tag1 -t tag1
```

Finally, if you want to produced ntuples (they can't be published at the CMS DAS) do:

```bash
python submit.py -s ntuples -E 5 10 15 -e 1.62 -p 22 -n 10 -u 1 -c campaign1 -i tag1 -t tag1
```
