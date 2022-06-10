import argparse

from pd_dwi.model import Model


def train(args):
    model = Model.from_config(args.config)
    model.train(args.dataset)
    model.save(args.out)


def predict(args):
    if args.out:
        assert args.out.endswith('.csv')

    model = Model.load(args.model)

    f_predict = model.predict_proba if args.probability else model.predict
    y_pred = f_predict(args.dataset)

    if args.out:
        y_pred.to_csv(args.out)
    else:
        print(y_pred)


def score(args):
    model = Model.load(args.model)
    score = model.score(args.dataset)
    print(f'{score:.4f}')


def pd_dwi_cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    parser_train = subparsers.add_parser('train')
    parser_train.add_argument('-dataset', type=str)
    parser_train.add_argument('-config', type=open)
    parser_train.add_argument('-out', type=str, required=False)
    parser_train.set_defaults(func=train)

    parser_predict = subparsers.add_parser('predict')
    parser_predict.add_argument('-model', type=str)
    parser_predict.add_argument('-dataset', type=str)
    parser_predict.add_argument('-probability', action='store_true')
    parser_predict.add_argument('-out', type=str)
    parser_predict.set_defaults(func=predict)

    parser_score = subparsers.add_parser('score')
    parser_score.add_argument('-model', type=str)
    parser_score.add_argument('-dataset', type=str)
    parser_score.set_defaults(func=score)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    pd_dwi_cli()
