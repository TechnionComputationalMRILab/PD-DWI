import click

from pd_dwi.scripts.adc_preprocess_command import adc_preprocess
from pd_dwi.scripts.list_command import list_available_models
from pd_dwi.scripts.predict_command import predict
from pd_dwi.scripts.score_command import score
from pd_dwi.scripts.train_command import train


@click.group(name='pd-dwi')
@click.version_option(message='version %(version)s')
def pd_dwi_cli() -> None:
    pass


pd_dwi_cli.add_command(list_available_models)
pd_dwi_cli.add_command(predict)
pd_dwi_cli.add_command(score)
pd_dwi_cli.add_command(train)


@click.group(name='pd-dwi-preprocessing')
@click.version_option(message='version %(version)s')
def preprocessing_cli() -> None:
    pass


preprocessing_cli.add_command(adc_preprocess)
