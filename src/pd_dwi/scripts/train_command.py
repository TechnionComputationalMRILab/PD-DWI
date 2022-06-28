from pd_dwi.model import Model


def train(args):
    model = Model.from_config(args.config)
    model.train(args.dataset)
    model.save(args.out)


def add_train_parser(parser):
    parser.add_argument('-dataset', type=str)
    parser.add_argument('-config', type=open)
    parser.add_argument('-out', type=str, required=False)
    parser.set_defaults(func=train)