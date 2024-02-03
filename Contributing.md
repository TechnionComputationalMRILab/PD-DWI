# Contributing

## How to setup local development environment

1. Install pipx - instructions are available [here](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
2. Install poetry via pipx 
    ```
    pipx install --suffix=@1.1.11 poetry==1.1.11
    ```
3. Clone PD-DWI project
    ```
    git clone https://github.com/TechnionComputationalMRILab/PD-DWI.git
    ```
4. Install project dependencies 
    ```
    poetry@1.1.11 install
    ```
5. Validate installation
    ```
    poetry@1.1.11 run pd-dwi --help
    ```