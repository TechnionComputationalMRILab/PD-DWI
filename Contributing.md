# Contributing

## How to setup local development environment

### Pre requisites

#### Pyenv

1. Install pyenv - instructions are available [here](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
2. Install python 3.9.21 via pyenv
   ```
   pyenv install 3.9.21
   ```

#### Poetry

1. Install pipx - instructions are available [here](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
2. Install poetry via pipx 
   ```
   pipx install --suffix=@2.1.1 poetry==2.1.1
   ```

### Install project

1. Clone PD-DWI project and access it
   ```
   git clone https://github.com/TechnionComputationalMRILab/PD-DWI.git
   cd PD-DWI 
   ```
2. Configure poetry to use python 3.9.21
   ```
   poetry@2.1.1 env use 3.9.21
   ```
3. Install project dependencies 
   ```
   poetry@2.1.1 install
   ```
4. Validate installation
   ```
   poetry@2.1.1 run pd-dwi --help
   ```