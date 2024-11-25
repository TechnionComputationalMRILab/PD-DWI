import os.path

import click

from pd_dwi.preprocessing.adc import ADCMap


@click.command(name='adc',
               help="Calculates an ADC from input DWI sequences and saves it in DWI folder."
                    "DATA_PATH can be used to run in either single or bulk mode."
                    "A text file path will enable the bulk mode.",
               )
@click.argument('data_path', type=click.Path(exists=True, file_okay=False))
@click.argument('b_values', nargs=-1, required=True, type=click.IntRange(min=0))
def adc_preprocess(data_path, b_values):
    adc = ADCMap(b_values)
    
    if os.path.isdir(data_path):
        folders = [data_path]
    else:
        print("Entering bulk mode.")
        with open(data_path, mode='r') as f:
            # Skip first line
            f.readline()
            folders = f.readlines()
                
    filename = f"ADC bVals={','.join(map(str, adc.b_values))}.dcm"
    for folder in folders:
        adc.transform(folder, os.path.join(data_path, filename))
