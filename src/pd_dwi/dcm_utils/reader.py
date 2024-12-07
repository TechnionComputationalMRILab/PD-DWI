from pathlib import Path
from typing import List, Union
from SimpleITK import ImageFileReader, ImageSeriesReader, GetArrayViewFromImage


class DicomReader(object):
    def __init__(self, file_name: Union[str, List[str]]):
        self._is_metadata_available = False
        self._reader = self._initialize_reader(file_name)
        self._image = None
        self._pixel_array = None
        
    def _initialize_reader(self, file_name: Union[str, List[str]]) -> Union[ImageFileReader, ImageSeriesReader]:
        """ Creates File reader from single input file """
        if isinstance(file_name, str) and Path(file_name).is_dir():
            file_name = list(Path(file_name).glob('*.dcm'))
        
        if isinstance(file_name, str):
            reader = ImageFileReader()
            reader.SetFileName(file_name)
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            self._is_metadata_available = True
        else:
            reader = ImageSeriesReader()
            reader.SetFileNames(file_name)
            reader.LoadPrivateTagsOn()
        
        return reader
    
    def _setup_metadata_functions(self):
        def metadata_decorator(func):
            def decorated_func(*args, **kwargs):
                self._execute_if_needed()
                
                try:
                    return func(*args, **kwargs)
                except RuntimeError as e:
                    if 'does not exist' not in str(e):
                        raise e
                else:
                    return None
            return decorated_func        
        
        for func_name in ['HasMetaDataKey', 'GetMetaDataKeys', 'GetMetaData']:
            setattr(self, func_name, metadata_decorator(getattr(self._reader, func_name)))


    def _execute_if_needed(self):
        if not self._is_metadata_available:
            self._image = self._reader.Execute()
            self._is_metadata_available = True
        
        return self._image


    @property
    def pixel_array(self):
        if self._pixel_array is None:
            self._image = self._execute_if_needed()
            self._pixel_array = GetArrayViewFromImage(self._image)
        return self._pixel_array
    
    @property
    def shape(self):
        return self._reader.GetSize()[::-1]
    
    @property
    def file_name(self):
        return self._reader.GetFileName()
    
    @property
    def file_names(self):
        return self._reader.GetFileNames()