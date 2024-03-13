from enum import Enum
from typing import List, Dict, Any, Optional, Set

from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt, root_validator, model_validator


class Labels(BaseModel):
    negative: str = Field(min_length=1)
    positive: str = Field(min_length=1)


class TimePoint(Enum):
    T0 = 'T0'
    T1 = 'T1'
    T2 = 'T2'


class Modality(Enum):
    ADC0100 = 'ADC 0100'
    ADC0100600800 = 'ADC 0100600800'
    ADC100600800 = 'ADC 100600800'
    F = 'F'


class Mask(Enum):
    DWI = 'DWI MASK'


class Dataset(BaseModel):
    labels: Labels
    time_points: Set[TimePoint] = Field(min_items=1)
    modalities: Set[Modality] = Field(min_items=1)
    masks: Set[Mask]


class RadiomicsFeaturesEncoder(BaseModel):
    image: Modality
    mask: Mask
    time_points: Set[TimePoint] = Field(min_items=1)


class RadiomicsFeaturesTransformer(BaseModel):
    encoders: List[RadiomicsFeaturesEncoder]
    engine: Dict[str, Any]


class FeatureTransformer(BaseModel):
    radiomics: RadiomicsFeaturesTransformer


class FeatureSelection(BaseModel):
    k: int


class Classifier(BaseModel):
    module: str
    parameters: Dict[str, Any]


class Pipeline(BaseModel):
    features_transformer: FeatureTransformer
    feature_selection: FeatureSelection
    classifier: Classifier


class GridSearchParamGrid(BaseModel):
    classifier: Dict[str, Any] = None
    feature_selection: Dict[str, Any] = None


class GridSearch(BaseModel):
    verbose: NonNegativeInt
    scoring: str = Field(default='roc_auc')
    cv: PositiveInt = Field(default=5)
    param_grid: GridSearchParamGrid


class ModelConfig(BaseModel):
    dataset: Dataset
    pipeline: Pipeline
    grid_search_cv: GridSearch = None

    class Config:
        frozen = True
        extra = 'forbid'

    @model_validator(mode='after')
    def validate_encoders_dataset(self):
        modalities = {e.image for e in self.pipeline.features_transformer.radiomics.encoders}

        if not modalities.issubset(self.dataset.modalities):
            raise ValueError("Encoders contain modalities that are not available in dataset")

        masks = {e.mask for e in self.pipeline.features_transformer.radiomics.encoders}

        if not masks.issubset(self.dataset.masks):
            raise ValueError("Encoders contain masks that are not available in dataset")

        return self