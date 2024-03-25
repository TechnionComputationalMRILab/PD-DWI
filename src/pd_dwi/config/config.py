try:
    from enum import StrEnum  # type: ignore
except ImportError:
    from strenum import StrEnum

from typing import List, Dict, Any, Set, Optional

from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt, model_validator, ConfigDict


class Labels(BaseModel):
    negative: str = Field(min_length=1)
    positive: str = Field(min_length=1)


class TimePoint(StrEnum):
    T0 = 'T0'
    T1 = 'T1'
    T2 = 'T2'


class Modality(StrEnum):
    ADC0100 = 'ADC 0100'
    ADC0100600800 = 'ADC 0100600800'
    ADC100600800 = 'ADC 100600800'
    F = 'F'


class Mask(StrEnum):
    DWI = 'DWI MASK'


class Dataset(BaseModel):
    labels: Labels
    time_points: Set[TimePoint] = Field(min_length=1)
    modalities: Set[Modality] = Field(min_length=1)
    masks: Set[Mask]


class RadiomicsFeaturesEncoder(BaseModel):
    image: Modality
    mask: Mask
    time_points: Set[TimePoint] = Field(min_length=1)


class RadiomicsFeaturesTransformer(BaseModel):
    encoders: List[RadiomicsFeaturesEncoder]
    engine: Optional[Dict[str, Any]] = None


class FeatureTransformer(BaseModel):
    radiomics: Optional[RadiomicsFeaturesTransformer] = None


class FeatureSelection(BaseModel):
    k: int


class Classifier(BaseModel):
    module: str
    parameters: Dict[str, Any]


class Pipeline(BaseModel):
    features_transformer: FeatureTransformer
    features_selection: FeatureSelection
    classifier: Classifier


class GridSearchParamGrid(BaseModel):
    classifier: Optional[Dict[str, Any]] = None
    features_selection: Optional[Dict[str, Any]] = None


class GridSearch(BaseModel):
    verbose: NonNegativeInt
    scoring: str = Field(default='roc_auc')
    cv: PositiveInt = Field(default=5)
    param_grid: GridSearchParamGrid


class ModelConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    dataset: Dataset
    pipeline: Pipeline
    grid_search_cv: Optional[GridSearch] = None

    @model_validator(mode='after')
    def validate_encoders_dataset(self) -> 'ModelConfig':
        if self.pipeline.features_transformer.radiomics:
            modalities = {e.image for e in self.pipeline.features_transformer.radiomics.encoders}

            if not modalities.issubset(self.dataset.modalities):
                raise ValueError("Encoders contain modalities that are not available in dataset")

            masks = {e.mask for e in self.pipeline.features_transformer.radiomics.encoders}

            if not masks.issubset(self.dataset.masks):
                raise ValueError("Encoders contain masks that are not available in dataset")

            time_points = self.pipeline.features_transformer.radiomics.encoders[0].time_points
            for e in self.pipeline.features_transformer.radiomics.encoders[1:]:
                time_points = time_points.union(e.time_points)

            if not time_points.issubset(self.dataset.time_points):
                raise ValueError("Encoders contain time points that are not available in dataset")

        return self
