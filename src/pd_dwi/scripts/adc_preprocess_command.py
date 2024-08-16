import os.path

import click

from pd_dwi.preprocessing.adc import calculate_adc


@click.command(name='adc',
               help="Calculates an ADC from input DWI sequences and saves it in DWI folder."
                    "DATA_PATH can be used to run in either single or bulk mode."
                    "A text file path will enable the bulk mode.",
               )
@click.argument('data_path', type=click.Path(exists=True, file_okay=False))
@click.argument('b', nargs=-1, required=True, type=click.IntRange(min=0))
def adc_preprocess(data_path, b):
    if os.path.isdir(data_path):
        calculate_adc(data_path, set(b), data_path)
    else:
        print("Entering bulk mode.")
        with open(data_path, mode='r') as f:
            # Skip first line
            f.readline()
            for dwi_folder in f.readlines():
                calculate_adc(dwi_folder, set(b), dwi_folder)
