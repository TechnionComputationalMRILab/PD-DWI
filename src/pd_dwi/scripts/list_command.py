import click

from pd_dwi.models import get_available_models


@click.command(name='list')
def list_available_models() -> None:
    """ Lists pre-trained model that are installed within the package. """
    models = get_available_models()

    for model_name, description in models.items():
        print(f'* {model_name}:\n\t{description}')

