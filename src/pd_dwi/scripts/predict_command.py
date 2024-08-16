import click

from pd_dwi.model import Model


@click.command()
@click.argument('model_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('dataset', type=click.Path(exists=True, file_okay=False))
@click.option('-probability', is_flag=True, type=bool, help="Retrieve prediction probability")
@click.option('-out', type=str, help="Path for prediction results file")
def predict(model_path, dataset, probability, out):
    """ Calculate model prediction for all subjects in input dataset.

    MODEL_PATH is the location of the model to use.
    """
    model = Model.load(model_path)

    f_predict = model.predict_proba if probability else model.predict
    y_pred = f_predict(dataset)

    if out:
        y_pred.to_csv(out)
    else:
        print(y_pred)
