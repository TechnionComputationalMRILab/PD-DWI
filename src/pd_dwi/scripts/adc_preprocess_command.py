import os.path
from typing import List

import click

from pd_dwi.preprocessing.adc import ADCMap


def validate_min_values(ctx, self, value):
    if len(value) < 2:
        raise click.BadParameter(f"Takes at least 2 values but {len(value)} was given", ctx=ctx, param=self)
    return value


@click.command(name='adc',
               help="Calculates an ADC from input DWI data",
               )
@click.option('-i', '--input', 'input_data', required=True, type=click.Path(exists=True, file_okay=False), help="Location of folder containing DWI dicom files.")
@click.option('-b', '--b-values', 'b_values', multiple=True, required=True, type=click.IntRange(min=0), callback=validate_min_values, help="List of b-values to calculate ADC from.")
@click.option('-o', '--output', 'output_data', required=False, type=click.Path(exists=True, file_okay=False), help="Location to save ADC at. If not provided, ADC will be saved in input folder.")
def adc_preprocess(input_data: str, b_values: List[int], output_data:str = None):
    print(b_values)
    exit()
    if output_data is None:
        output_data = input_data
    
    adc = ADCMap(b_values)
    
    if os.path.isdir(input_data):
        folders = [input_data]
    else:
        print("Entering bulk mode.")
        with open(input_data, mode='r') as f:
            # Skip first line
            f.readline()
            folders = f.readlines()
                
    filename = f"ADC bVals={','.join(map(str, adc.b_values))}.dcm"
    for folder in folders:
        adc.transform(folder, os.path.join(input_data, filename))
