from pd_dwi.model import Model


def train(args):
    model = Model.from_config(args.config)
    model.train(args.dataset)
    model.save(args.out)


def add_train_parser(parser):
    parser.add_argument('-dataset', type=str, required=True, help='Path for dataset to use')
    parser.add_argument('-config', type=open, required=True, help='Path for config to use')
    parser.add_argument('-out', type=str, required=True, help='Path for storing the trained model')
    parser.set_defaults(func=train)
