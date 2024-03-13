from pd_dwi.model import Model


def score(args):
    score = Model.load(args.model).score(args.dataset)
    print(f'{score:.4f}')


def add_score_parser(parser):
    parser.add_argument('-model', type=str, required=True, help="Path for model name to load")
    parser.add_argument('-dataset', type=str, required=True, help="Path for dataset to use")
    parser.set_defaults(func=score)
