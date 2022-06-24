import argparse

from pd_dwi.scripts.list_command import add_list_parser
from pd_dwi.scripts.predict_command import add_predict_parser
from pd_dwi.scripts.score_command import add_score_parser
from pd_dwi.scripts.train_command import add_train_parser


def pd_dwi_cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    add_train_parser(subparsers.add_parser('train'))
    add_predict_parser(subparsers.add_parser('predict'))
    add_score_parser(subparsers.add_parser('score'))
    add_list_parser(subparsers.add_parser('list'))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    pd_dwi_cli()
