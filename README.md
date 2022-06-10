# PD-DWI

## Dataset structure

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
