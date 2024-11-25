from typing import Tuple, Union


class DicomTag(object):
    def __init__(self, key: Union[Tuple[str], Tuple[int]], base=10):
        if base != 10:
            assert all(isinstance(item, str) for item in key)
            key = tuple([int(item, base) for item in key])
        
        self._key = key
        
    @property
    def key(self):
        return self._key
        
    def __str__(self):
        return f"{self.key[0]:04x}|{self.key[1]:04x}"
        

class DicomHeader:
    image_type = DicomTag((0x0008, 0x0008))
    
    study_date = DicomTag((0x0008, 0x0020))
    series_date = DicomTag((0x0008, 0x0021))
    acquision_date = DicomTag((0x0008, 0x0022))
    
    study_time = DicomTag((0x0008, 0x0030))
    series_time = DicomTag((0x0008, 0x0031))
    acquision_time = DicomTag((0x0008, 0x0032))
    
    study_description = DicomTag((0x0008, 0x1030))
    series_description = DicomTag((0x0008, 0x103e))

    patient_id = DicomTag((0x0010, 0x0020))

    b_value = DicomTag((0x0018, 0x9087))

    comment = DicomTag((0x0020, 0x4000))
    
    rescale_intercept = DicomTag((0x0028,0x1052))
    rescale_slope = DicomTag((0x0028, 0x1053))
    rescale_type = DicomTag((0x0028, 0x1054))
