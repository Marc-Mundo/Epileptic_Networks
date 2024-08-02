# Installation Instructions

## Prerequisites

- Git
- Conda (Preferably: Miniconda)
- Code editor (Preferably: Visual Studio Code)
- Python 3.7 or higher (Preferably: Python 3.9)
- Jupyter Notebook
- Neuron Simulator

## Cloning the Repository

First, clone the repository using SSH:

```bash
git clone git@github.com:SynapticaNL/Marc_network_sims.git
cd Marc_network_sims
```

## Initializing Submodule

You will need the Sanjay2015 model from model DB to use as a base for the experiments. This is included as a submodule in the repository. To initialize the submodule, run:

```bash
git submodule init
git submodule update
```

## Creating the `neuromics` conda environment

Create a new Conda environment named neuromics using the neuromics.yml file:

```bash
conda env create -f neuromics.yml
```

This file contains all the necessary packages for the project and the appropriate versions.

## Activating the Environment

Once the environment is successfully created, activate it:

```bash
conda activate neuromics
```

You are now ready to run the code in the neuromics environment.

## Neuromics module

```bash
cd /home/USER/neuromics
pip install -r requirements.txt
```

## Installing NEURON mod files

You will need to compile the Sanjay2015 model mod files to use them in your simulations. To do this, run from Marc_network_sims directory:

```bash
cd /Models/Sanjay_model  # submodule which contains the mod files
nrnivmodl *.mod  # compiles the mod files
```

This will make the mod files available for use in your simulations.
The actual Cell and network classes are in the SynapticaSims directory of the neuromics repository.

## Experiments

You can run experiments scripts from the `Experiments` directory. For example, run the `Exp02_baseline.py` script while in the neuromics conda environment to initialize the NEURON simulation for the baseline experiment (second experiment in the series).

```bash
python Exp02_baseline.py
```

See the `Exp_params.json` file in the Experiments directory for the parameters used in the experiments.

## Notebooks

You can use the Jupyter Notebooks in the `Notebooks` directory to analyze the data generated from the experiments.

Some experiments depend on processing scripts which paired with the notebooks (Experiments 5 & 6).
