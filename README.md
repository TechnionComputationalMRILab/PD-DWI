# PD-DWI

PD-DWI is a physiologically-decomposed Diffusion-Weighted MRI machine-learning model for predicting response to neoadjuvant chemotherapy in invasive breast cancer.

PD-DWI was developed by [TCML](https://tcml-bme.github.io/) group as part of [BMMR2 challenge](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=89096426) using [ACRIN-6698](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=50135447) dataset.

PD-DWI model was accepted to MICCAI 2022:

```
M. Gilad, M. Freiman. PD-DWI: Predicting response to neoadjuvant chemotherapy in invasive breast cancer with Physiologically-Decomposed Diffusion-Weighted MRI machine-learning model. Medical Image Computing and Computer Assisted Intervention – MICCAI 2022 to be held during Sept 18-22 in Singapore.
```

# Installation

PD-DWI model can be installed directly from Github: 

```
git clone https://github.com/TechnionComputationalMRILab/PD-DWI.git
cd PD-DWI
python setup.py install
```

# Usage

PD-DWI can be used in a Python script or via command line.

## CLI

To explore all options and syntax requirements run `pd-dwi --help` in your terminal.

### Training

```
pd-dwi train -d DATASET_FOLDER -c CONFIG_YAML -o OUTPUT_PKL_PATH
```

Model training requires that

1. DATASET_FOLDER is created according to [dataset structure guidlines](docs/dataset.md)
2. CONFIG_YAML is created according to [configuration scheme](docs/configuration.md)

### Predict

```
pd-dwi predict -m PKL_PATH -d DATASET_FOLDER
```

# Contact

Please contact us on ms.maya.gilad@gmail.com