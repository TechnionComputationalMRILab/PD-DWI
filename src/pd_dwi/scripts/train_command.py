import click

from pd_dwi.model import Model


@click.command()
@click.argument('dataset', type=click.Path(exists=True, file_okay=False))
@click.argument('config', type=click.Path(exists=True, dir_okay=False))
@click.argument('out', type=click.Path(exists=False))
def train(dataset, config, out):
    """ Train a new model. """
    model = Model.from_config(config)
    model.train(dataset)
    model.save(out)
