import os.path

from pd_dwi.preprocessing.adc import calculate_adc


def adc_preprocess(args):
    input_data = args.dwi_data
    b_values = args.b

    if os.path.isdir(input_data):
        calculate_adc(input_data, set(b_values), input_data)
    else:
        with open(input_data, mode='r') as f:
            # Skip first line
            f.readline()
            for dwi_folder in f.readlines():
                calculate_adc(dwi_folder, set(b_values), dwi_folder)


def add_adc_parser(parser) -> None:
    parser.add_argument('-dwi_data', type=str, required=True, help="Path for DWI acquisition folder or input file listing DWI folders")
    parser.add_argument('-b', type=int, nargs='+', required=True, help="B-values to use for ADC calculation")

    parser.set_defaults(func=adc_preprocess)
