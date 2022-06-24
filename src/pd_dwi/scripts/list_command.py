from pd_dwi.models import get_available_models


def list_available_models(args):
    models = get_available_models()
    print(models)


def add_list_parser(parser):
    parser.set_defaults(func=list_available_models)
