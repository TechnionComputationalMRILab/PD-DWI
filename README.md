# PD-DWI

# Setup

PD-DWI model can be installed directly from github using 

```
git clone https://github.com/TechnionComputationalMRILab/PD-DWI.git
cd PD-DWI
python setup.py install
```

After the PD-DWI is installed, you will be able to import it in your code, or use the cli

# CLI

PD-DWI provides a cli to train, predict and score your model on any given dataset.

To explore all options and syntax requirements run `pd-dwi --help` in your terminal.

## Training

```
pd-dwi train -d DATASET_FOLDER -c CONFIG_YAML -o OUTPUT_PKL_PATH
```

Model training requires that

1. DATASET_FOLDER is created according to [dataset structure guidlines](docs/dataset.md)
2. CONFIG_YAML is created according to [configuration scheme](docs/configuration.md)

## Predict

```
pd-dwi predict -m PKL_PATH -d DATASET_FOLDER
```
