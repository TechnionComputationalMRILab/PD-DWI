from math import log10
from pathlib import Path
from typing import List, Union
from SimpleITK import GetImageFromArray, WriteImage

from pd_dwi.dcm_utils.reader import DicomReader
from pd_dwi.dcm_utils.tags import DicomHeader


class DicomWriter(object):
    def __init__(self, path: str):
        """ Constructor

        Args:
            path (str): Output path of Dicom file
        """
        if Path(path).exists:
            raise FileExistsError(path)
        
        self._path = path
        self._image = None
        
    def __enter__(self):
        return self
    
    def __exit__(self):
        self.save()
        
    def save(self):
        Path(self._path).parent.mkdir(parents=True, exist_ok=True)
        WriteImage(self._image, self._path)
    
    def image(self, image_array, multiply_by=1.0):
        self._image = GetImageFromArray(image_array * multiply_by)
        
        self._image.SetMetaData(DicomHeader.rescale_intercept, "0")
        self._image.SetMetaData(DicomHeader.rescale_slope, str(1 / multiply_by))
        
        if multiply_by != 1.0:
            self._image.SetMetaData(DicomHeader.rescale_intercept, f"10^{-log10(multiply_by):.0f}mm^2/s")
    
    def metadata_like(self, reader: Union[str, DicomReader]):
        if isinstance(reader, str): 
            reader = DicomReader(reader)
        
        self._image.CopyInformation(reader.image)
        
        copy_tags = [
            DicomHeader.patient_id, 
            DicomHeader.study_description,
            DicomHeader.study_date, DicomHeader.series_date, DicomHeader.acquision_date,
            DicomHeader.study_time, DicomHeader.series_time, DicomHeader.acquision_time
        ]
        
        for tag in copy_tags:
            if not reader.HasMetaDataKey(tag):
                continue
            self._image.SetMetaData(tag, reader.image.GetMetaData(tag))
            
    def series_description(self, value):
        self._image.SetMetaData(DicomHeader.series_description, value)
        
    def comment(self, value):
        self._image.SetMetaData(DicomHeader.comment, value)
    
    def image_type(self, types: List[str]):
        types_as_str = "\\".join(types)
        self._image.SetMetaData(DicomHeader.image_type, types_as_str)
    