# Contributing

## How to setup local development environment

### Pre requisites

#### Pyenv

1. Install pyenv - instructions are available [here](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
2. Install python 3.8.13 via pyenv
   ```
   pyenv install 3.8.13
   ```

#### Poetry

1. Install pipx - instructions are available [here](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
2. Install poetry via pipx 
   ```
   pipx install --suffix=@1.8.4 poetry==1.8.4
   ```

### Install project

1. Clone PD-DWI project and access it
   ```
   git clone https://github.com/TechnionComputationalMRILab/PD-DWI.git
   cd PD-DWI 
   ```
2. Configure poetry to use python 3.8.13
   ```
   poetry@1.8.4 env use 3.8.13
   ```
3. Install project dependencies 
   ```
   poetry@1.8.4 install
   ```
4. Validate installation
   ```
   poetry@1.8.4 run pd-dwi --help
   ```