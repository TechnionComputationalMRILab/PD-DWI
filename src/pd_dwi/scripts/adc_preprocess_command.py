import os.path

import click

from pd_dwi.preprocessing.adc import calculate_adc


@click.command(name='adc')
@click.argument('dwi_data', type=click.Path(exists=True, file_okay=False))
@click.argument('b', nargs=-1, required=True, type=click.IntRange(min=0))
def adc_preprocess(dwi_data, b):
    """ Calculates ADC from input DWI sequences and saves it in DWI folder. """
    if os.path.isdir(dwi_data):
        calculate_adc(dwi_data, set(b), dwi_data)
    else:
        with open(dwi_data, mode='r') as f:
            # Skip first line
            f.readline()
            for dwi_folder in f.readlines():
                calculate_adc(dwi_folder, set(b), dwi_folder)
