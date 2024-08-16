# Install Package

## Install via pip

PD-DWI package is available on PyPi for installation via pip. Wheels are automatically generated for each release of PD-DWI, allowing you to
install pd-dwi without having to compile anything. 

!!! note
    Ensure that you have python 3.8 installed on your machine.

* Install PD-DWI:
    ```bash
    python -m pip install pd-dwi
    ```

## Install from source

PD-DWI can also be installed from source code.

!!! note
    Ensure the following pre-prerequisites are installed on your machine:

    * git
    * python 3.8
    * poetry 1.8.3

1. Clone the repository
```console
    git clone https://github.com/TechnionComputationalMRILab/PD-DWI.git
```
2. Install the project
```console
  cd PD-DWI & poetry install --all-extras
```