# particleGun
Scripts for easy and multiple MC samples generation.

```bash
wget https://raw.githubusercontent.com/chrispap95/particleGun/master/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_11_1_0_pre6
cd CMSSW_11_1_0_pre6/src
cmsenv
cd particleGun
```

## Instructions
First, create the generator fragment destination in ```src```
```bash
mkdir -p Configuration/GenProduction/python
scram b
```
To make a new MC generation, create a new directory in ```src```. Eg.
```bash
mkdir singleGammaMC
cd singleGammaMC
```

Then clone the repository
```bash
git clone https://github.com/chrispap95/particleGun.git
cd particleGun
```

Now, submit step1 (GEN-SIM) by issuing:
```bash
python step1.py -E 5 10 15 -e 1p7 -p 22 -n 10 -u 50
```
That is going to submit single gamma (```-p 22```) at energies 5, 10, 15 GeV (```-E 5 10 15```) and eta 1.7 (```-e 1p7```). For each energy and eta, the script submits 10 jobs (```-n 10```) with 50 events each (```-u 50```). To see the options available:
```bash
python step1.py --help
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
