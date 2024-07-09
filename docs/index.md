# Welcome to PD-DWI documentation!

PD-DWI is a physiologically-decomposed Diffusion-Weighted MRI machine-learning model for predicting response to neoadjuvant chemotherapy in invasive breast cancer.

PD-DWI was developed by [TCML](https://tcml-bme.github.io/) group. 

<figure markdown="span">
    ![TCML](assets/tcml.png)
</figure>

**If you publish any work which uses this package, please cite the following publication:** Gilad, M., Freiman, M. (2022). PD-DWI: Predicting Response to Neoadjuvant Chemotherapy in Invasive Breast Cancer with Physiologically-Decomposed Diffusion-Weighted MRI Machine-Learning Model. In: Wang, L., Dou, Q., Fletcher, P.T., Speidel, S., Li, S. (eds) Medical Image Computing and Computer Assisted Intervention – MICCAI 2022. MICCAI 2022. Lecture Notes in Computer Science, vol 13433. Springer, Cham. https://doi.org/10.1007/978-3-031-16437-8_4

!!! note
    This work was developed as part of the [BMMR2 challenge](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=89096426) using [ACRIN-6698](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=50135447) dataset.

!!! warning
    Not intended for clinical use. 

## BMMR2 Challenge 

``` plotly
{
    "data": [
        {
            "x": [
                "Benchmark",
                "Team C",
                "Team B",
                "Team A",
                "PD-DWI"
            ],
            "y": [
                0.782,
                0.803,
                0.838,
                0.840,
                0.885
            ],
            "type": "bar"
        }
    ],
    "layout": {
        "yaxis": {
            "range": [
                0.75,
                1
            ]
        }
    }
}
```

