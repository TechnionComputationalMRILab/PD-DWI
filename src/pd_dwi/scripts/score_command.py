import click

from pd_dwi.model import Model


@click.command()
@click.option('-m', '--model', 'model_path', required=True, type=click.Path(exists=True, dir_okay=False), help="Location of saved model.")
@click.option('-d', '--dataset', 'dataset', required=True, type=click.Path(exists=True, file_okay=False), help="Location of dataset.")
def score(model_path: str, dataset: str):
    """ Evaluate model performance on a given dataset. """
    score = Model.load(model_path).score(dataset)
    print(f'{score:.4f}')
