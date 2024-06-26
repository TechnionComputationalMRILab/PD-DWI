import argparse
from typing import List, Optional

from pd_dwi.scripts.adc_preprocess_command import add_adc_parser
from pd_dwi.scripts.list_command import add_list_parser
from pd_dwi.scripts.predict_command import add_predict_parser
from pd_dwi.scripts.score_command import add_score_parser
from pd_dwi.scripts.train_command import add_train_parser


def pd_dwi_cli(input_args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    add_train_parser(subparsers.add_parser('train'))
    add_predict_parser(subparsers.add_parser('predict'))
    add_score_parser(subparsers.add_parser('score'))
    add_list_parser(subparsers.add_parser('list'))

    args = parser.parse_args(input_args)
    args.func(args)


def preprocessing_cli(input_args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='cmd', required=True)

    add_adc_parser(subparsers.add_parser('adc'))

    args = parser.parse_args(input_args)
    args.func(args)


if __name__ == '__main__':
    pd_dwi_cli()
