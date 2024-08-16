import click

from pd_dwi.model import Model


@click.command()
@click.argument('model_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('dataset', type=click.Path(exists=True, file_okay=False))
def score(model_path, dataset):
    """ Evaluate model performance on a given dataset. """
    score = Model.load(model_path).score(dataset)
    print(f'{score:.4f}')
