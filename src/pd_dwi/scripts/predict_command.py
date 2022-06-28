import os.path
from sys import stderr

from pd_dwi.model import Model
from pd_dwi.models import get_model_path_by_name


def predict(args):
    if args.out:
        assert args.out.endswith('.csv')

    if os.path.exists(args.model):
        model_path = args.model
    else:
        model_path = get_model_path_by_name(args.model)

    if model_path is None:
        print(f'Could not locate {args.model}, please check model exists', file=stderr)
        exit(1)

    model = Model.load(model_path)

    f_predict = model.predict_proba if args.probability else model.predict
    y_pred = f_predict(args.dataset)

    if args.out:
        y_pred.to_csv(args.out)
    else:
        print(y_pred)


def add_predict_parser(parser):
    parser.add_argument('-model', type=str)
    parser.add_argument('-dataset', type=str)
    parser.add_argument('-probability', action='store_true')
    parser.add_argument('-out', type=str)
    parser.set_defaults(func=predict)