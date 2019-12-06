# particleGun
Scripts for easy and multiple MC samples generation.

## Instructions
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

Now submit step1 (GEN-SIM) by issuing:
```bash
python step1.py -E 5 10 15 -e 1p7 -p 22 -n 10 -u 50
```

To see the options available:
```bash
python step1.py --help
```
