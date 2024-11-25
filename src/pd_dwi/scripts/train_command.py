import click

from pd_dwi.model import Model


@click.command()
@click.option('-d', '--dataset', 'dataset', required=True, type=click.Path(exists=True, file_okay=False), help="Location of dataset.")
@click.option('-c', '--config', 'config', required=True, type=click.Path(exists=True, dir_okay=False), help="Location of training configuration.")
@click.option('-o', '--output', 'output', required=True, type=click.Path(exists=False, file_okay=True), help="Location to save model after training completion.")
def train(dataset, config, output):
    """ Train a new model. """
    model = Model.from_config(config)
    model.train(dataset)
    model.save(output)
