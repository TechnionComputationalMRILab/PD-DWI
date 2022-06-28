# Dataset

## Structure

    .
    ├── train                       # Training dataset 
    │   ├── clinical.csv            # Clinical information of subjects
    │   ├── subject X               # Subject imaging modalities
    │   │   ├── T0                  # Subject modalities acquired at T0 
    │   │   │   ├── MASK.dcm        # Diffusion Weighted Imaging mask
    │   │   │   ├── F.dcm           # Diffusion Fraction volume
    │   │   │   ├── ADC 0100.dcm    # ADC of b-values 0-100 volume
    │   │   │   └── ...
    │   │   └── ...
    │   └── ...
    ├── test                        # Testing dataset
    │   ├── clinical.csv            
    │   ├── subject Y               
    └── ...


## Clinical information

The clinical.csv must contain the following attributes: 
1. Patient ID DICOM - subject identifier, must be identical to subject's folder name
2. hrher4g - 4 level hormone receptor status
3. SBRgrade - 3 level tumor grade 
4. race - subject's race
5. Ltype - lesion type
6. pcr - pCR label of subject. If not available, should be defined as an empty string