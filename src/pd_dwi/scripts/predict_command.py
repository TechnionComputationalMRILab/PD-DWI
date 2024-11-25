import click

from pd_dwi.model import Model


@click.command()
@click.option('-m', '--model', 'model_path', required=True, type=click.Path(exists=True, dir_okay=False), help="Location of saved model.")
@click.option('-d', '--dataset', 'dataset', required=True, type=click.Path(exists=True, file_okay=False), help="Location of dataset.")
@click.option('-p', '-probability', 'probability', is_flag=True, type=bool, help="Retrieve prediction probability.")
@click.option('-o', '--output', 'output', type=click.Path(exists=False, file_okay=True), help="Output path to store prediction results in.")
def predict(model_path: str, dataset: str, probability: bool, output: str):
    """ Calculate model prediction for all subjects in input dataset.

    MODEL_PATH is the location of the model to use.
    """
    model = Model.load(model_path)

    f_predict = model.predict_proba if probability else model.predict
    y_pred = f_predict(dataset)

    if output:
        y_pred.to_csv(output)
    else:
        print(y_pred)
