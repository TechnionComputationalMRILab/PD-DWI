from pd_dwi.model import Model


def score(args):
    score = Model.load(args.model).score(args.dataset)
    print(f'{score:.4f}')


def add_score_parser(parser):
    parser.add_argument('-model', type=str)
    parser.add_argument('-dataset', type=str)
    parser.set_defaults(func=score)