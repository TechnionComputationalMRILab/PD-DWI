from pd_dwi.models import get_available_models


def list_available_models(args):
    models = get_available_models()

    for model_name, description in models.items():
        print(f'* {model_name}:\n\t{description}')


def add_list_parser(parser):
    parser.set_defaults(func=list_available_models)
