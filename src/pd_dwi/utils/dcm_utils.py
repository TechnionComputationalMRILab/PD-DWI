from typing import Union, List, Optional

from SimpleITK import ImageFileReader, ImageSeriesReader, Image
from pydicom import FileDataset


def create_file_reader(file_name):
    """ Creates File reader from single input file """

    reader = ImageFileReader()
    reader.SetFileName(file_name)
    reader.LoadPrivateTagsOn()

    return reader


def copy_metadata_from_image_series_reader(reader: Union[ImageSeriesReader, ImageFileReader],
                                           output_image: Image,
                                           user_ignore_keys: Optional[List[str]] = None):
    """ Copies series-level tags from reader to output image """
    ignore_keys = ['0020|0013', '0020|0032', '0020|1041'] + (user_ignore_keys or [])

    if isinstance(reader, ImageSeriesReader):
        for key in reader.GetMetaDataKeys(0):
            if key in ignore_keys:
                continue

            output_image.SetMetaData(key, reader.GetMetaData(0, key))
    else:
        for key in reader.GetMetaDataKeys():
            if key in ignore_keys:
                continue

            output_image.SetMetaData(key, reader.GetMetaData(key))


def read_b_value(dcm: FileDataset):
    """ Read b-value tag from input dicom """
    return int(dcm[0x0018, 0x9087].value)
