from interface import train
from interface import generate

import numpy as np


def main():
    params = {
        'family': 'autoencoder',
        'input_col': 'X',
        'output_col': 'X',
        'model': {
            'name': 'rnn_rnn_autoencoder',
            'params':{
                'encode_nb_hidden_units': [128],
                'latent_nb_hidden_units': [32],
                'latent_activations': ['linear'],
                'decode_nb_hidden_units': [128],
                'rnn_type': 'GRU',
                'output_activation': {'name': 'axis_softmax' , 'params': {'axis': 'time_features'}}
             }
        },
        'data': {
            'train': {
                'pipeline':[
                    {"name": "load_numpy", 
                     "params": {"filename": "./data/zinc12.npz", "cols": ["X"], "nb": 100000}},
                ]
            },
            'transformers':[
                {'name': 'DocumentVectorizer', 'params': {'length': 120, 'onehot': True}}
            ]
        },
        'report':{
            'outdir': 'out',
            'checkpoint': {
                'loss': 'train_categorical_crossentropy',
                'save_best_only': True
            },
            'metrics': ['categorical_crossentropy'],
            'domain_specific': []
        },
        'optim':{
            'algo': {
                'name': 'adam',
                'params': {'lr': 1e-3}
            },
            'lr_schedule':{
                'name': 'constant',
                'params': {}
            },
            'early_stopping':{
                'name': 'none',
                'params': {
                    'patience_loss': 'categorical_crossentropy',
                    'patience': 5
                }
            },
            'max_nb_epochs': 100,
            'batch_size': 128,
            'pred_batch_size': 128,
            'loss': 'categorical_crossentropy',
            'budget_secs': 86400,
            'seed': 42
        },
    }
    train(params)
    params = {
        'model':{
            'folder': 'out'
        },
        'method':{
            'name': 'iterative_refinement',
            'params': {
                'batch_size': 128,
                'nb_samples': 256,
                'nb_iter': 5,
                'binarize':{
                    'name': 'none',
                    'params': {
                    }
                },
                'noise':{
                    'name': 'none',
                    'params': {}
                },
                'stop_if_unchanged': True,
                'seed': 42
            },
            'save_folder': 'out/gen',
        }
    }
    generate(params)
    data = np.load('out/gen/generated.npz')
    print(data['generated'])

if __name__ == '__main__':
    main()