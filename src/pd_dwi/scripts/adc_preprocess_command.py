from pd_dwi.preprocessing.adc import calculate_adc


def adc_preprocess(args):
    dwi_folder_path = args.dwi_folder
    b_values = args.b

    calculate_adc(dwi_folder_path, set(b_values), dwi_folder_path)


def add_adc_parser(parser) -> None:
    parser.add_argument('-dwi_folder', type=str, required=True, help="Path for DWI acquisition folder")
    parser.add_argument('-b', type=int, nargs='+', required=True, help="B-values to use for ADC calculation")

    parser.set_defaults(func=adc_preprocess)
