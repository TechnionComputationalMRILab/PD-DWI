# Getting Started

## Dataset setup

PD-DWI model training and inference expects a specific folders and files structure

    .
    ├── train                       # Training dataset 
    │   ├── clinical.csv            # Clinical information of subjects
    │   ├── subject X               # Subject imaging modalities
    │   │   ├── T0                  # Subject modalities acquired at T0 
    │   │   │   ├── ADC 0100.dcm    # ADC calculated from b-values 0-100
    │   │   │   ├── F.dcm           # Diffusion Fraction volume
    │   │   │   ├── MASK.dcm        # Diffusion Weighted Imaging mask
    │   │   │   └── ...
    │   │   └── ...
    │   └── ...
    ├── test                        # Testing dataset
    │   ├── clinical.csv            
    │   ├── subject Y               
    └── ...

### Imaging data

As shown in above structure, imaging data is stored by subject id and acquision time.

Our PD-DWI framework requires at least one DWI-based map, accompanied by a MASK which represents the tumor ROI.
It is assumed that tumor MASK is corresponding to the DWI-based map, and available in the same spacing.
The DWI-based map can be either ADC or F, or both. 

To calculate the ADC and F maps from your DWI data, please use our pre-processing utility. 

### Clinical data

All clinical data will be stored in a file named _clinical.csv_. 
Each line will contain the following values, by order of appearance: 

1. Patient ID DICOM - subject identifier, must be identical to subject's folder name
2. hrher4g - 4 level hormone receptor status
3. SBRgrade - 3 level tumor grade 
4. race - subject's race
5. Ltype - lesion type
6. pcr - pCR label of subject. If not available, should be defined as an empty string