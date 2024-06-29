# Dataset Preprocessing 

## ADC Calculation

### Single Map 

To calculate an ADC map, run:

!!! note ""
    pd-dwi-preprocessing adc -dwi_data <path/to/DWI/data\> -b <list/of/b/values\>

### Batch Mode

To calculate an ADC map for a large number of folders, run:

!!! note ""
    pd-dwi-preprocessing adc -dwi_data <path/to/input/file\> -b <list/of/b/values\>

The input file for ADC batch processing is a CSV file where the first row contains a header (skipped in processing), and each subsequent row represents a path for a DWI acquisition folder.